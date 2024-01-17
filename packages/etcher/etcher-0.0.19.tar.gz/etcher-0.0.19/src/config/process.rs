use std::collections::{HashMap, HashSet};

use bitbazaar::{cli::run_cmd, err, errors::TracedErr, timeit};
use log::{debug, info};
use serde::Serialize;

use super::{engine::Engine, raw_conf::RawConfig};
use crate::args::RenderCommand;

#[derive(Debug, Serialize)]
pub struct Config {
    pub context: HashMap<String, serde_json::Value>,
    pub exclude: Vec<String>,
    pub engine: Engine,
    pub ignore_files: Vec<String>,
    pub setup_commands: Vec<String>,
}

pub fn process(raw: RawConfig, render_args: &RenderCommand) -> Result<Config, TracedErr> {
    let mut context: HashMap<String, serde_json::Value> = HashMap::new();

    // Before anything else, run the setup commands:
    for command in raw.setup_commands.iter() {
        info!("Running command: {}", command);
        let cmd_out = timeit!(format!("Setup cmd: {}", command).as_str(), {
            run_cmd(command)
        })?;

        info!("{}", cmd_out.stdout);

        if cmd_out.code != 0 {
            return Err(err!(
                "Setup command '{}' returned non zero exit code: {}",
                command,
                cmd_out.code
            ));
        }
    }

    for (key, value) in raw.context.stat {
        context.insert(key, value.consume()?);
    }

    // Now env vars:

    // If some env defaults banned, validate list and convert to a hashset for faster lookup:
    let banned_env_defaults: Option<HashSet<String>> = if let Some(banned) =
        render_args.ban_defaults.as_ref()
    {
        // If no vars provided, ban all defaults:
        if banned.is_empty() {
            Some(raw.context.env.keys().cloned().collect::<HashSet<String>>())
        } else {
            let banned_env_defaults: HashSet<String> = banned.iter().cloned().collect();
            // Make sure they are all valid env context keys:
            for key in banned_env_defaults.iter() {
                if !raw.context.env.contains_key(key) {
                    // Printing the env keys in the error, want them alphabetically sorted:
                    let mut env_keys = raw
                        .context
                        .env
                        .keys()
                        .map(|s| s.as_str())
                        .collect::<Vec<&str>>();
                    env_keys.sort_by_key(|name| name.to_lowercase());
                    return Err(err!(
                        "Unrecognized context.env var provided to '--ban-defaults': '{}'. All env vars in config: '{}'.",
                        key, env_keys.join(", ")
                    ));
                }
            }
            Some(banned_env_defaults)
        }
    } else {
        None
    };

    for (key, value) in raw.context.env {
        context.insert(
            key.clone(),
            value.consume(
                &key,
                // Check if the default is banned:
                if let Some(banned) = banned_env_defaults.as_ref() {
                    banned.contains(key.as_str())
                } else {
                    false
                },
            )?,
        );
    }

    // External commands can be extremely slow compared to the rest of the library,
    // try and remedy a bit by running them in parallel:
    let mut handles = vec![];
    for (key, value) in raw.context.cli {
        handles.push(std::thread::spawn(
            move || -> Result<(String, serde_json::Value), TracedErr> {
                let value = value.consume()?;
                Ok((key, value))
            },
        ));
    }

    for handle in handles {
        let (key, value) = handle.join().unwrap()?;
        context.insert(key, value);
    }

    let config = Config {
        context,
        exclude: raw.exclude,
        engine: raw.engine,
        ignore_files: raw.ignore_files,
        setup_commands: raw.setup_commands,
    };

    debug!("Processed config: \n{:#?}", config);

    Ok(config)
}
