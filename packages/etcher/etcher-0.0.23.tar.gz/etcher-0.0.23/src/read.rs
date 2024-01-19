use std::collections::HashSet;

use bitbazaar::{err, errors::TracedErr};

use crate::{
    args::{ReadConfigCommand, ReadOutputFormat, ReadVarCommand},
    config::final_config_path,
};

/// Read specific contents from the config file. Prints as json.
pub fn read_config(args: &crate::args::Args, read: &ReadConfigCommand) -> Result<(), TracedErr> {
    // This will error if can't be found:
    let config_path = final_config_path(&args.config, None)?;
    let toml_contents = std::fs::read_to_string(config_path)?;

    let target =
        crate::utils::toml::read(&toml_contents, &read.path.split('.').collect::<Vec<&str>>())?;

    // Handle different output formats:
    match read.output {
        ReadOutputFormat::Raw => match target {
            serde_json::Value::String(s) => println!("{}", s),
            target => println!("{}", serde_json::to_string(&target)?),
        },
        ReadOutputFormat::Json => println!("{}", serde_json::to_string_pretty(&target)?),
    }

    Ok(())
}

/// Read a finalised config variable.
pub fn read_var(args: &crate::args::Args, read: &ReadVarCommand) -> Result<(), TracedErr> {
    let raw_conf = crate::config::RawConfig::from_toml(&final_config_path(&args.config, None)?)?;

    let all_context_keys = raw_conf.all_context_keys();

    let conf = crate::config::process(
        raw_conf,
        None,
        // Don't need to compute all of them, just the one being printed:
        Some(HashSet::from_iter([read.var.as_str()])),
        false,
    )?;

    if let Some(target) = conf.context.get(read.var.as_str()) {
        // Handle different output formats:
        match read.output {
            ReadOutputFormat::Raw => match target {
                serde_json::Value::String(s) => println!("{}", s),
                target => println!("{}", serde_json::to_string(&target)?),
            },
            ReadOutputFormat::Json => println!("{}", serde_json::to_string_pretty(&target)?),
        }
        Ok(())
    } else {
        Err(err!(
            "Context variable '{}' not found in finalised config. All context keys: '{}'.",
            read.var,
            all_context_keys.join(", ")
        ))
    }
}
