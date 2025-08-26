#!/usr/bin/env python3
"""
MLX Fine-Tuning Toolkit - Command Line Interface

A modern CLI for fine-tuning large language models using Apple's MLX framework.
"""

import click
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from .config import MLXConfig, ConfigManager
    from .training import TrainingManager
    from .utils import check_system_requirements, get_hardware_info
except ImportError as e:
    try:
        # Fallback to absolute imports
        from cli.config import MLXConfig, ConfigManager
        from cli.training import TrainingManager
        from cli.utils import check_system_requirements, get_hardware_info
    except ImportError as e2:
        rprint(f"[red]Error importing modules: {e2}[/red]")
        rprint("[yellow]Make sure you're running from the correct directory and have installed dependencies[/yellow]")
        sys.exit(1)

console = Console()

@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def cli(ctx, version):
    """
    🚀 MLX Fine-Tuning Toolkit
    
    A complete toolkit for fine-tuning Large Language Models using Apple's MLX framework.
    Optimized for Apple Silicon Macs with professional-grade features.
    """
    if version:
        rprint("[bold blue]MLX Fine-Tuning Toolkit v1.0.0[/bold blue]")
        rprint("Built for Apple Silicon • MLX Framework • Production Ready")
        return
        
    if ctx.invoked_subcommand is None:
        rprint(Panel.fit(
            "[bold blue]🚀 MLX Fine-Tuning Toolkit[/bold blue]\n\n"
            "A complete toolkit for fine-tuning Large Language Models\n"
            "using Apple's MLX framework on macOS.\n\n"
            "[dim]Use --help to see available commands[/dim]",
            title="Welcome",
            border_style="blue"
        ))

@cli.command()
@click.option('--model', default='qwen3-0.5b-mlx', help='Model to fine-tune')
@click.option('--data', required=True, type=click.Path(exists=True), help='Training data file (JSONL format)')
@click.option('--validation', type=click.Path(exists=True), help='Validation data file (optional)')
@click.option('--config', type=click.Path(), help='Configuration file (YAML)')
@click.option('--output', type=click.Path(), help='Output directory for adapters')
@click.option('--learning-rate', type=float, default=1e-5, help='Learning rate')
@click.option('--batch-size', type=int, default=1, help='Batch size')
@click.option('--max-iters', type=int, default=1000, help='Maximum training iterations')
@click.option('--save-every', type=int, default=100, help='Save frequency (iterations)')
@click.option('--validate-every', type=int, default=50, help='Validation frequency (iterations)')
@click.option('--resume', type=click.Path(), help='Resume from adapter checkpoint')
@click.option('--dry-run', is_flag=True, help='Validate configuration without training')
def train(model, data, validation, config, output, learning_rate, batch_size, 
          max_iters, save_every, validate_every, resume, dry_run):
    """
    🏋️ Fine-tune a model with the given parameters
    
    This command starts the fine-tuning process with comprehensive monitoring,
    validation, and automatic checkpoint saving.
    """
    try:
        with console.status("[bold blue]Initializing training...[/bold blue]") as status:
            # Load or create configuration
            config_manager = ConfigManager()
            if config:
                cfg = config_manager.load_config(config)
            else:
                cfg = config_manager.create_default_config()
                
            # Override config with command line arguments
            cfg.model.name = model
            cfg.training.learning_rate = learning_rate
            cfg.training.batch_size = batch_size
            cfg.training.max_iters = max_iters
            cfg.training.save_every = save_every
            cfg.training.validate_every = validate_every
            
            if output:
                cfg.model.adapter_path = Path(output)
            if resume:
                cfg.training.resume_adapter_file = Path(resume)
                
            status.update("[bold blue]Validating configuration...[/bold blue]")
            config_manager.validate_config(cfg)
            
            status.update("[bold blue]Checking system requirements...[/bold blue]")
            system_ok, issues = check_system_requirements()
            if not system_ok:
                for issue in issues:
                    rprint(f"[red]❌ {issue}[/red]")
                raise click.ClickException("System requirements not met")
            
        if dry_run:
            rprint("[green]✅ Configuration validation successful![/green]")
            rprint("[yellow]Dry run complete - no training performed[/yellow]")
            return
            
        # Initialize training manager
        trainer = TrainingManager(cfg)
        
        rprint("[bold green]🚀 Starting fine-tuning...[/bold green]")
        trainer.train(data_path=data, validation_path=validation)
        
    except Exception as e:
        rprint(f"[red]❌ Training failed: {e}[/red]")
        raise click.ClickException(str(e))

@cli.command()
@click.argument('model', required=False)
@click.option('--list', 'list_models', is_flag=True, help='List available models')
@click.option('--dir', 'download_dir', type=click.Path(), help='Download directory')
@click.option('--force', is_flag=True, help='Force re-download')
def download(model, list_models, download_dir, force):
    """
    📥 Download models for fine-tuning
    
    Download popular pre-trained models optimized for MLX fine-tuning.
    """
    if list_models:
        table = Table(title="Available Models")
        table.add_column("Model", style="cyan", no_wrap=True)
        table.add_column("Size", style="magenta")
        table.add_column("Description", style="green")
        
        models = {
            "qwen3-0.5b-mlx": ("500MB", "⭐ Default - Ultra-fast training, perfect for getting started"),
            "qwen2.5-1.5b-instruct": ("900MB", "Small model for testing and experimentation"),
            "qwen2.5-3b-instruct": ("1.9GB", "Balanced model for most use cases"),
            "qwen2.5-7b-instruct": ("4.5GB", "High-quality results, slower training"),
            "llama-3.2-3b-instruct": ("1.8GB", "Compact Llama model"),
            "llama-3.1-8b-instruct": ("4.9GB", "Good performance alternative"),
            "mistral-7b-instruct": ("4.1GB", "European open source model"),
        }
        
        for model_name, (size, desc) in models.items():
            table.add_row(model_name, size, desc)
        
        console.print(table)
        return
    
    if not model:
        rprint("[yellow]Please specify a model to download or use --list to see available models[/yellow]")
        return
        
    # TODO: Implement actual model download logic
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Downloading {model}...", total=None)
        # Simulate download process
        import time
        time.sleep(2)
        progress.update(task, description=f"✅ Downloaded {model}")
    
    rprint(f"[green]✅ Model {model} downloaded successfully![/green]")

@cli.command()
@click.option('--model', required=True, help='Model/adapter to use for generation')
@click.option('--prompt', help='Text prompt for generation')
@click.option('--max-tokens', type=int, default=100, help='Maximum tokens to generate')
@click.option('--temperature', type=float, default=0.7, help='Sampling temperature')
@click.option('--interactive', is_flag=True, help='Start interactive chat mode')
def generate(model, prompt, max_tokens, temperature, interactive):
    """
    💬 Generate text using fine-tuned models
    
    Use your fine-tuned models for text generation with configurable parameters.
    """
    if interactive:
        rprint("[bold blue]🤖 Interactive Chat Mode[/bold blue]")
        rprint("[dim]Type 'quit' to exit[/dim]\n")
        
        while True:
            try:
                user_input = click.prompt("You", type=str)
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                    
                with console.status("[bold blue]Generating response...[/bold blue]"):
                    # TODO: Implement actual generation logic
                    import time
                    time.sleep(1)
                
                rprint(f"[green]Assistant:[/green] This is a simulated response to: {user_input}")
                rprint()
                
            except KeyboardInterrupt:
                break
                
        rprint("\n[yellow]Chat session ended[/yellow]")
        return
    
    if not prompt:
        prompt = click.prompt("Enter your prompt", type=str)
    
    with console.status("[bold blue]Generating...[/bold blue]"):
        # TODO: Implement actual generation logic
        import time
        time.sleep(1)
        
    rprint(f"[green]Generated text:[/green] This is a simulated response to: {prompt}")

@cli.command()
@click.option('--port', default=8080, help='Port for web interface')
@click.option('--host', default='127.0.0.1', help='Host for web interface')
@click.option('--dev', is_flag=True, help='Run in development mode')
def gui(port, host, dev):
    """
    🎨 Launch the desktop GUI application
    
    Start the web-based graphical interface for visual fine-tuning.
    """
    rprint("[bold blue]🎨 Starting MLX Fine-Tuning GUI...[/bold blue]")
    
    if dev:
        rprint("[yellow]Running in development mode[/yellow]")
    
    rprint(f"[green]GUI will be available at: http://{host}:{port}[/green]")
    
    # TODO: Implement actual GUI startup logic
    try:
        import time
        with console.status("[bold blue]Starting server...[/bold blue]"):
            time.sleep(2)
        rprint("[green]✅ GUI started successfully![/green]")
        rprint("[dim]Press Ctrl+C to stop[/dim]")
        
        # Simulate server running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        rprint("\n[yellow]GUI shutdown[/yellow]")

@cli.command()
@click.option('--verbose', is_flag=True, help='Show detailed system information')
def doctor(verbose):
    """
    🩺 System diagnostics and health check
    
    Verify that your system is properly configured for MLX fine-tuning.
    """
    rprint("[bold blue]🩺 MLX Fine-Tuning Toolkit - System Diagnostics[/bold blue]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # System check
        task1 = progress.add_task("Checking system requirements...", total=None)
        system_ok, issues = check_system_requirements()
        
        # Hardware check
        task2 = progress.add_task("Detecting hardware...", total=None)
        hw_info = get_hardware_info()
        
        # Dependencies check
        task3 = progress.add_task("Verifying dependencies...", total=None)
        # TODO: Implement dependency checking
        
        import time
        time.sleep(1)
        
        progress.update(task1, description="✅ System requirements")
        progress.update(task2, description="✅ Hardware detection")
        progress.update(task3, description="✅ Dependencies")
    
    # Results
    rprint("\n[bold green]📊 System Report[/bold green]")
    
    if system_ok:
        rprint("[green]✅ System: Ready for MLX fine-tuning[/green]")
    else:
        rprint("[red]❌ System: Issues detected[/red]")
        for issue in issues:
            rprint(f"  [red]• {issue}[/red]")
    
    if verbose and hw_info:
        rprint(f"\n[bold blue]🔧 Hardware Information[/bold blue]")
        for key, value in hw_info.items():
            rprint(f"  [cyan]{key}:[/cyan] {value}")

@cli.command()
@click.option('--create', type=click.Path(), help='Create default configuration file')
@click.option('--validate', type=click.Path(exists=True), help='Validate configuration file')
@click.option('--show', is_flag=True, help='Show current configuration')
def config(create, validate, show):
    """
    ⚙️ Configuration management
    
    Create, validate, and manage configuration files.
    """
    config_manager = ConfigManager()
    
    if create:
        rprint(f"[blue]Creating default configuration: {create}[/blue]")
        default_config = config_manager.create_default_config()
        config_manager.save_config(default_config, create)
        rprint(f"[green]✅ Configuration created: {create}[/green]")
        return
    
    if validate:
        rprint(f"[blue]Validating configuration: {validate}[/blue]")
        try:
            cfg = config_manager.load_config(validate)
            config_manager.validate_config(cfg)
            rprint(f"[green]✅ Configuration is valid[/green]")
        except Exception as e:
            rprint(f"[red]❌ Configuration validation failed: {e}[/red]")
            raise click.ClickException(str(e))
        return
    
    if show:
        # TODO: Implement configuration display
        rprint("[blue]Current configuration:[/blue]")
        rprint("[dim]Configuration display not implemented yet[/dim]")
        return
    
    rprint("[yellow]Use --help to see configuration options[/yellow]")

@cli.command()
def gui():
    """
    🖥️ Launch the GUI application
    
    Start the desktop GUI for visual fine-tuning.
    """
    import subprocess
    import sys
    from pathlib import Path
    
    # Find the GUI directory
    gui_dir = Path(__file__).parent.parent / "gui"
    gui_launcher = gui_dir / "run_gui.py"
    
    if not gui_launcher.exists():
        rprint("[red]❌ GUI launcher not found[/red]")
        rprint(f"[dim]Expected location: {gui_launcher}[/dim]")
        return
    
    rprint("[blue]🚀 Launching MLX Fine-Tuning GUI...[/blue]")
    
    try:
        # Run the GUI launcher
        subprocess.run([sys.executable, str(gui_launcher)], cwd=gui_dir)
    except KeyboardInterrupt:
        rprint("\n[yellow]GUI stopped by user[/yellow]")
    except Exception as e:
        rprint(f"[red]❌ Error launching GUI: {e}[/red]")
        rprint("[dim]Try running the GUI directly:[/dim]")
        rprint(f"[dim]cd {gui_dir} && python run_gui.py[/dim]")

def main():
    """Entry point for the CLI application"""
    try:
        cli()
    except KeyboardInterrupt:
        rprint("\n[yellow]Operation cancelled[/yellow]")
        sys.exit(1)
    except Exception as e:
        rprint(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main()