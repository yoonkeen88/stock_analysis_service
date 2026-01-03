"""
Generate database schema diagram as PNG image
Requires: pip install eralchemy
Alternative: Use mermaid-cli (npm install -g @mermaid-js/mermaid-cli)
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from eralchemy import render_er
    ERALCHEMY_AVAILABLE = True
except ImportError:
    ERALCHEMY_AVAILABLE = False
    print("⚠️  eralchemy not installed. Install with: pip install eralchemy")
    print("   Or use mermaid-cli: npm install -g @mermaid-js/mermaid-cli")

from app.core.database import engine
from app.db.models import Base


def generate_image_with_eralchemy():
    """Generate PNG image using eralchemy"""
    if not ERALCHEMY_AVAILABLE:
        print("❌ eralchemy is not available")
        return False
    
    output_file = Path(__file__).parent.parent / "docs" / "schema.png"
    output_file.parent.mkdir(exist_ok=True)
    
    try:
        render_er(Base, str(output_file))
        print(f"✅ Schema image generated: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return False


def generate_image_with_mermaid_cli():
    """Generate PNG using mermaid-cli (requires npm)"""
    import subprocess
    
    mermaid_file = Path(__file__).parent.parent / "docs" / "SCHEMA_AUTO.md"
    output_file = Path(__file__).parent.parent / "docs" / "schema.png"
    
    if not mermaid_file.exists():
        print(f"❌ Mermaid file not found: {mermaid_file}")
        print("   Run generate_schema_diagram.py first")
        return False
    
    try:
        # Extract mermaid code from markdown
        with open(mermaid_file, "r") as f:
            content = f.read()
            mermaid_code = content.split("```mermaid\n")[1].split("\n```")[0]
        
        # Save temporary mermaid file
        temp_mermaid = Path(__file__).parent.parent / "docs" / "temp_schema.mmd"
        with open(temp_mermaid, "w") as f:
            f.write(mermaid_code)
        
        # Run mermaid-cli
        result = subprocess.run(
            ["mmdc", "-i", str(temp_mermaid), "-o", str(output_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Schema image generated: {output_file}")
            temp_mermaid.unlink()  # Clean up
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ mermaid-cli not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main function"""
    print("Generating database schema image...")
    print("\nOptions:")
    print("1. Using eralchemy (Python)")
    print("2. Using mermaid-cli (Node.js)")
    
    # Try eralchemy first
    if ERALCHEMY_AVAILABLE:
        if generate_image_with_eralchemy():
            return
    
    # Fallback to mermaid-cli
    print("\nTrying mermaid-cli...")
    if generate_image_with_mermaid_cli():
        return
    
    print("\n💡 To generate images, install one of:")
    print("   - eralchemy: pip install eralchemy")
    print("   - mermaid-cli: npm install -g @mermaid-js/mermaid-cli")


if __name__ == "__main__":
    main()

