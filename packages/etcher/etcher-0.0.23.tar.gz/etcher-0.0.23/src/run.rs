use bitbazaar::{
    errors::TracedErr,
    logging::{create_subscriber, SubLayer, SubLayerFilter, SubLayerVariant},
    timing::GLOBAL_TIME_RECORDER,
};
use clap::{Parser, Subcommand};
use tracing::debug;

use crate::{
    args::{self, get_py_args, get_version_info},
    init, read, render, ETCH_ROOT_ARGS,
};

pub fn run() -> Result<(), TracedErr> {
    let mut py_args = get_py_args()?;

    // Clap doesn't support default subcommands but we want to run `render` by
    // default for convenience, so we just preprocess the arguments accordingly before passing them to Clap.
    let arg1 = py_args.get(1);
    let add = {
        if let Some(arg1) = arg1 {
            // If the first argument isn't already a subcommand, and isn't a specific root arg/option, true:
            !args::Command::has_subcommand(arg1) && !ETCH_ROOT_ARGS.contains(&arg1.as_str())
        } else {
            true
        }
    };
    if add {
        py_args.insert(1, "render".into());
    }

    let args = args::Args::parse_from(py_args);

    // Setup global logging:
    let mut log_layers: Vec<SubLayer> = vec![];
    if args.log_level_args.verbose {
        log_layers.push(SubLayer {
            variant: SubLayerVariant::Stdout {},
            filter: SubLayerFilter::Above(tracing::Level::TRACE),
            ..Default::default()
        });
    } else if !args.log_level_args.silent {
        // If its a read command (i.e. the output is important, only show errors, to prevent polluting the output)
        if matches!(
            &args.command,
            args::Command::ReadConfig(_) | args::Command::ReadVar(_)
        ) {
            log_layers.push(SubLayer {
                variant: SubLayerVariant::Stdout {},
                filter: SubLayerFilter::Above(tracing::Level::ERROR),
                ..Default::default()
            });
        } else {
            // Otherwise by default show info and up:

            // For INFO, don't show the level:
            log_layers.push(SubLayer {
                variant: SubLayerVariant::Stdout {},
                filter: SubLayerFilter::Only(vec![tracing::Level::INFO]),
                include_lvl: false,
                ..Default::default()
            });

            // For the rest, show the level:
            log_layers.push(SubLayer {
                variant: SubLayerVariant::Stdout {},
                filter: SubLayerFilter::Above(tracing::Level::WARN),
                ..Default::default()
            });
        }
    }

    create_subscriber(log_layers)?.into_global();

    let result = match &args.command {
        args::Command::Render(render) => {
            render::render(&args, render)?;
            Ok(())
        }
        args::Command::ReadConfig(read_config) => Ok(read::read_config(&args, read_config)?),
        args::Command::ReadVar(read_var) => Ok(read::read_var(&args, read_var)?),
        args::Command::Init(init) => Ok(init::init(init)?),
        args::Command::Version { output_format: _ } => {
            println!("etch {}", get_version_info());
            Ok(())
        }
    };

    debug!("{}", GLOBAL_TIME_RECORDER.format_verbose()?);

    result
}
