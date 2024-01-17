use bitbazaar::errors::TracedErr;

use crate::{
    args::{ReadCommand, ReadOutputFormat},
    config::final_config_path,
};

/// Read specific contents from the config file. Prints as json.
pub fn read_config(args: &crate::args::Args, read: &ReadCommand) -> Result<(), TracedErr> {
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
