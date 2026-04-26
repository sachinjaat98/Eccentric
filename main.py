"""
Main Application Entry Point

This module initializes and runs the Eccentric application.
It sets up logging, configuration, and Flask API server.

Usage:
    python main.py [--host HOST] [--port PORT] [--debug]

Examples:
    # Run with default settings
    python main.py
    
    # Run with custom host and port
    python main.py --host 0.0.0.0 --port 8000
    
    # Run in debug mode
    python main.py --debug
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config.settings import (
        API_HOST,
        API_PORT,
        DEBUG,
        LOG_LEVEL,
        APP_NAME,
        VERSION
    )
    from config.logger import setup_logging
    from src.app import create_app
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure all dependencies are installed: pip install -r config/requirements.txt")
    sys.exit(1)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} v{VERSION} - Text Recognition and Translation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Run with default settings
  python main.py --host 0.0.0.0 --port 8000  # Custom host/port
  python main.py --debug                   # Debug mode
        """
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default=API_HOST,
        help=f'Server host (default: {API_HOST})'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=API_PORT,
        help=f'Server port (default: {API_PORT})'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='Number of workers (default: 1)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'{APP_NAME} {VERSION}'
    )
    
    return parser.parse_args()


def print_banner():
    """Print application banner."""
    banner = f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          {APP_NAME.center(55)}║
    ║          Text Recognition & Multilingual Translation     ║
    ║                                                           ║
    ║          Version: {VERSION:<43}║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """Check if all required dependencies are installed."""
    logger = logging.getLogger(__name__)
    
    required_packages = [
        'cv2',
        'pytesseract',
        'googletrans',
        'gtts',
        'flask',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"❌ Missing required packages: {', '.join(missing_packages)}")
        logger.info("Install them with: pip install -r config/requirements.txt")
        return False
    
    logger.info("✅ All dependencies are installed")
    return True


def check_external_tools():
    """Check if external tools (Tesseract) are available."""
    logger = logging.getLogger(__name__)
    
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        logger.info("✅ Tesseract OCR is installed")
        return True
    except Exception as e:
        logger.warning(f"⚠️  Tesseract OCR not found: {e}")
        logger.warning("OCR features will not be available")
        logger.info("Install Tesseract: sudo apt-get install tesseract-ocr")
        return False


def verify_directories():
    """Verify and create necessary directories."""
    logger = logging.getLogger(__name__)
    
    directories = [
        'logs',
        'output',
        'data',
        'models'
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ Created directory: {directory}/")
            except Exception as e:
                logger.error(f"❌ Failed to create directory {directory}: {e}")
                return False
    
    return True


def main():
    """Main application entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Print banner
    print_banner()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check dependencies
    logger.info("Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Check external tools
    check_external_tools()
    
    # Verify directories
    logger.info("Verifying directories...")
    if not verify_directories():
        sys.exit(1)
    
    # Create Flask app
    try:
        logger.info("Initializing Flask application...")
        app = create_app()
    except Exception as e:
        logger.error(f"❌ Failed to initialize application: {e}", exc_info=True)
        sys.exit(1)
    
    # Log startup information
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {APP_NAME} v{VERSION}")
    logger.info("=" * 60)
    logger.info(f"Host: {args.host}")
    logger.info(f"Port: {args.port}")
    logger.info(f"Debug: {args.debug}")
    logger.info(f"Log Level: {LOG_LEVEL}")
    logger.info("=" * 60)
    logger.info("📚 Documentation: https://github.com/sachinjaat98/Eccentric/docs")
    logger.info("🐛 Report issues: https://github.com/sachinjaat98/Eccentric/issues")
    logger.info("=" * 60)
    
    try:
        # Run Flask application
        logger.info(f"✅ Application started successfully")
        logger.info(f"🌐 API available at: http://{args.host}:{args.port}")
        logger.info(f"📊 Health check: http://{args.host}:{args.port}/api/health")
        
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            threaded=True,
            use_reloader=args.debug
        )
        
    except KeyboardInterrupt:
        logger.info("⏹️  Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
