"""
MLX Fine-Tuning Toolkit - Configuration Management

Unified configuration system with hardware auto-detection and validation.
"""

import os
import yaml
import platform
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List, Union
import logging

logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Model configuration settings"""
    name: str = "qwen2.5-7b-instruct"
    cache_dir: str = "~/.mlx-models"
    adapter_path: Optional[str] = None
    trust_remote_code: bool = False
    revision: str = "main"
    
@dataclass
class TrainingConfig:
    """Training hyperparameters and settings"""
    learning_rate: float = 1e-5
    batch_size: int = 1
    max_iters: int = 1000
    save_every: int = 100
    validate_every: int = 50
    max_seq_length: int = 1024
    gradient_accumulation_steps: int = 1
    warmup_steps: int = 0
    weight_decay: float = 0.01
    gradient_checkpointing: bool = True
    resume_adapter_file: Optional[str] = None
    early_stopping_patience: int = 3
    
@dataclass
class DataConfig:
    """Data processing configuration"""
    validation_split: float = 0.1
    shuffle: bool = True
    max_length: int = 1024
    truncation: bool = True
    padding: str = "max_length"
    
@dataclass
class HardwareConfig:
    """Hardware optimization settings"""
    device: str = "mps"
    mixed_precision: bool = True
    compile_model: bool = False
    use_metal: bool = True
    max_memory_mb: Optional[int] = None
    
@dataclass
class LoggingConfig:
    """Logging and monitoring configuration"""
    log_level: str = "INFO"
    log_dir: str = "~/.mlx-finetuning/logs"
    log_file: str = "training.log"
    logging_steps: int = 10
    tensorboard_dir: Optional[str] = None
    wandb_project: Optional[str] = None
    
@dataclass
class GUIConfig:
    """GUI application settings"""
    host: str = "127.0.0.1"
    port: int = 8080
    auto_open_browser: bool = True
    theme: str = "dark"
    update_interval: int = 1000

@dataclass
class MLXConfig:
    """Complete MLX fine-tuning configuration"""
    model: ModelConfig = None
    training: TrainingConfig = None
    data: DataConfig = None
    hardware: HardwareConfig = None
    logging: LoggingConfig = None
    gui: GUIConfig = None
    
    def __post_init__(self):
        """Initialize nested configs if not provided"""
        if self.model is None:
            self.model = ModelConfig()
        if self.training is None:
            self.training = TrainingConfig()
        if self.data is None:
            self.data = DataConfig()
        if self.hardware is None:
            self.hardware = HardwareConfig()
        if self.logging is None:
            self.logging = LoggingConfig()
        if self.gui is None:
            self.gui = GUIConfig()

class ConfigManager:
    """Configuration management with validation and auto-detection"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".mlx-finetuning"
        self.config_dir.mkdir(exist_ok=True)
        
    def detect_hardware(self) -> Dict[str, Any]:
        """Detect hardware capabilities and optimize settings"""
        hardware_info = {}
        
        try:
            # Check if on macOS
            if platform.system() != "Darwin":
                logger.warning("MLX is optimized for macOS")
                hardware_info["platform"] = platform.system()
                return hardware_info
                
            # Check for Apple Silicon
            result = subprocess.run(
                ["sysctl", "-n", "hw.optional.arm64"], 
                capture_output=True, text=True, check=False
            )
            is_apple_silicon = result.returncode == 0 and result.stdout.strip() == "1"
            hardware_info["apple_silicon"] = is_apple_silicon
            
            if not is_apple_silicon:
                logger.warning("Apple Silicon recommended for optimal performance")
            
            # Get memory information
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"], 
                capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                memory_bytes = int(result.stdout.strip())
                memory_gb = memory_bytes // (1024**3)
                hardware_info["memory_gb"] = memory_gb
                
                # Recommend memory limits based on available RAM
                if memory_gb >= 64:
                    hardware_info["recommended_max_memory_mb"] = 32768  # 32GB
                elif memory_gb >= 32:
                    hardware_info["recommended_max_memory_mb"] = 16384  # 16GB
                else:
                    hardware_info["recommended_max_memory_mb"] = memory_gb * 512  # Half of RAM
            
            # Check MLX availability
            try:
                import mlx.core as mx
                hardware_info["mlx_available"] = True
                hardware_info["mlx_device_count"] = 1  # MLX uses unified memory
            except ImportError:
                hardware_info["mlx_available"] = False
                logger.error("MLX not installed. Install with: pip install mlx")
                
        except Exception as e:
            logger.error(f"Hardware detection failed: {e}")
            
        return hardware_info
    
    def create_default_config(self) -> MLXConfig:
        """Create default configuration with hardware auto-detection"""
        hardware_info = self.detect_hardware()
        
        config = MLXConfig()
        
        # Apply hardware-specific optimizations
        if hardware_info.get("apple_silicon"):
            config.hardware.device = "mps"
            config.hardware.use_metal = True
        else:
            config.hardware.device = "cpu"
            config.hardware.use_metal = False
            
        if "recommended_max_memory_mb" in hardware_info:
            config.hardware.max_memory_mb = hardware_info["recommended_max_memory_mb"]
            
        # Expand paths
        config.model.cache_dir = str(Path(config.model.cache_dir).expanduser())
        config.logging.log_dir = str(Path(config.logging.log_dir).expanduser())
        
        return config
    
    def load_config(self, config_path: Union[str, Path]) -> MLXConfig:
        """Load configuration from YAML file"""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f)
                
            # Create config objects from nested dictionaries
            model_config = ModelConfig(**config_dict.get('model', {}))
            training_config = TrainingConfig(**config_dict.get('training', {}))
            data_config = DataConfig(**config_dict.get('data', {}))
            hardware_config = HardwareConfig(**config_dict.get('hardware', {}))
            logging_config = LoggingConfig(**config_dict.get('logging', {}))
            gui_config = GUIConfig(**config_dict.get('gui', {}))
            
            config = MLXConfig(
                model=model_config,
                training=training_config,
                data=data_config,
                hardware=hardware_config,
                logging=logging_config,
                gui=gui_config
            )
            
            # Expand paths
            config.model.cache_dir = str(Path(config.model.cache_dir).expanduser())
            config.logging.log_dir = str(Path(config.logging.log_dir).expanduser())
            if config.model.adapter_path:
                config.model.adapter_path = str(Path(config.model.adapter_path).expanduser())
                
            return config
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")
        except TypeError as e:
            raise ValueError(f"Invalid configuration format: {e}")
    
    def save_config(self, config: MLXConfig, config_path: Union[str, Path]):
        """Save configuration to YAML file"""
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config_dict = asdict(config)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                
            logger.info(f"Configuration saved to {config_path}")
            
        except Exception as e:
            raise ValueError(f"Failed to save configuration: {e}")
    
    def validate_config(self, config: MLXConfig) -> bool:
        """Validate configuration settings"""
        errors = []
        
        # Validate model settings
        if not config.model.name:
            errors.append("Model name cannot be empty")
            
        # Validate training settings
        if config.training.learning_rate <= 0:
            errors.append("Learning rate must be positive")
            
        if config.training.batch_size <= 0:
            errors.append("Batch size must be positive")
            
        if config.training.max_iters <= 0:
            errors.append("Max iterations must be positive")
            
        if config.training.max_seq_length <= 0:
            errors.append("Max sequence length must be positive")
            
        # Validate data settings
        if not 0 < config.data.validation_split < 1:
            errors.append("Validation split must be between 0 and 1")
            
        # Validate paths
        model_cache_dir = Path(config.model.cache_dir)
        if not model_cache_dir.parent.exists():
            errors.append(f"Model cache directory parent does not exist: {model_cache_dir.parent}")
            
        log_dir = Path(config.logging.log_dir)
        if not log_dir.parent.exists():
            errors.append(f"Log directory parent does not exist: {log_dir.parent}")
        
        # Validate hardware settings
        if config.hardware.device not in ["cpu", "mps", "cuda"]:
            errors.append("Device must be one of: cpu, mps, cuda")
            
        if config.hardware.max_memory_mb is not None and config.hardware.max_memory_mb <= 0:
            errors.append("Max memory must be positive if specified")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ValueError(error_msg)
            
        return True
    
    def get_config_template(self, level: str = "basic") -> str:
        """Get configuration template as YAML string"""
        if level == "basic":
            return """# MLX Fine-Tuning Toolkit - Basic Configuration

model:
  name: "qwen2.5-7b-instruct"
  cache_dir: "~/.mlx-models"

training:
  learning_rate: 1.0e-5
  batch_size: 1
  max_iters: 1000
  save_every: 100
  validate_every: 50
  max_seq_length: 1024

data:
  validation_split: 0.1
  max_length: 1024
  
hardware:
  device: "mps"  # Use "cpu" for non-Apple Silicon
  mixed_precision: true
  
logging:
  log_level: "INFO"
  logging_steps: 10
"""
        else:  # advanced
            config = self.create_default_config()
            return yaml.dump(asdict(config), default_flow_style=False, indent=2)