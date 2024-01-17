use std::path::PathBuf;

use bitbazaar::{err, errors::TracedErr};
use clap::{command, Parser};
use pyo3::Python;

pub static DEFAULT_CONFIG_PATH: &str = "./etch.config.toml";

/// Get the args from python rather than rust, works better:
pub fn get_py_args() -> Result<Vec<String>, TracedErr> {
    Python::with_gil(|py| {
        Ok::<_, TracedErr>(
            py.import("sys")?
                .getattr("argv")?
                .extract::<Vec<String>>()?,
        )
    })
}

// Create the version info string, used in multiple places so need to centralize logic.
pub fn get_version_info() -> String {
    let inner = || {
        let py_args = get_py_args()?;
        let bin_path = py_args
            .first()
            .ok_or_else(|| err!("Failed to get binary path from args: '{:?}'.", py_args))?
            .clone();
        Ok::<_, TracedErr>(format!("{} ({})", env!("CARGO_PKG_VERSION"), bin_path))
    };
    match inner() {
        Ok(s) => s,
        Err(e) => {
            format!("Failed to get version info: {}", e)
        }
    }
}

#[derive(Debug, Parser)]
#[command(
    author,
    name = "etch",
    about = "Etch: An extremely fast metaprogrammer.",
    after_help = "For help with a specific command, see: `etch help <command>`."
)]
#[command(version = get_version_info())]
pub struct Args {
    #[command(subcommand)]
    pub command: Command,
    #[clap(flatten)]
    pub log_level_args: bitbazaar::logging::ClapLogLevelArgs,
    /// The config file to use. Note if render command, relative and not found from working directory, will search entered root directory.
    #[arg(
        short,
        long,
        global = true,
        default_value = DEFAULT_CONFIG_PATH,
        help = "The config file to use."
    )]
    pub config: PathBuf,
}

#[derive(Debug, clap::Subcommand)]
pub enum Command {
    /// Render all templates found whilst traversing the given root (default).
    Render(RenderCommand),
    /// Initialize the config file in the current directory.
    Init(InitCommand),
    /// Read specific contents from the config file. Prints as json.
    Read(ReadCommand),
    /// Display Etch's version
    Version {
        #[arg(long, value_enum, default_value = "text")]
        output_format: HelpFormat,
    },
}

#[derive(Clone, Debug, clap::Parser)]
pub struct RenderCommand {
    /// The target directory to search and render.
    #[clap(default_value = ".")]
    pub root: PathBuf,
    /// Force write all rendered files, ignore existing lockfile.
    #[arg(short, long, default_value = "false")]
    pub force: bool,
    /// Comma separated list of env ctx vars to ignore defaults for and raise if not in env. E.g. --ban-defaults FOO,BAR...
    ///
    /// If no vars are provided, all defaults will be ignored.
    ///
    /// Useful in e.g. a production build where you expect env vars to be available.
    #[clap(short, long, value_delimiter = ',', num_args = 0..)]
    pub ban_defaults: Option<Vec<String>>,
    /// Hidden test flag, writes some json output to the root dir.
    #[arg(long, default_value = "false", hide = true)]
    pub debug: bool,
}

#[derive(Parser, Debug, Clone, clap::ValueEnum)]
#[clap(rename_all = "lowercase")]
pub enum ReadOutputFormat {
    Raw,
    Json,
}

#[derive(Clone, Debug, clap::Parser)]
pub struct ReadCommand {
    /// The target directory to search and render.
    #[clap(
        default_value = ".",
        help = "The '.' separated path to search in the config file. E.g. 'context.env.foo.default' or '.' for the whole config."
    )]
    pub path: String,
    /// The output format to print in.
    ///
    /// - raw (default) -> same as json except simple string output is printed without quotes, to allow for easier command chaining.
    ///
    /// - json -> json compatible output.
    #[arg(short, long, default_value = "raw")]
    pub output: ReadOutputFormat,
}

#[derive(Clone, Debug, clap::Parser)]
pub struct InitCommand {}

#[derive(Debug, Clone, Copy, clap::ValueEnum)]
pub enum HelpFormat {
    Text,
    Json,
}
