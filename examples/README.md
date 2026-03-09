# Sleepwalker Protocol Examples

This directory contains examples demonstrating how to use the Sleepwalker Protocol (SWP) in your applications.

## Python Examples

### Basic Example
`basic_example.py` - Demonstrates basic SWP usage with various emotional states.

```bash
python examples/basic_example.py
```

### TOI Integration Example
`toi_integration.py` - Shows how to integrate SWP with a user's Terms of Interaction (TOI) configuration.

```bash
python examples/toi_integration.py
```

### Crisis Detection Example
`crisis_detection.py` - Demonstrates how SWP detects and responds to crisis indicators.

```bash
python examples/crisis_detection.py
```

## Configuration Example

### Sample TOI Configuration
`sample_toi.yaml` - A sample Terms of Interaction configuration file showing all available options.

Copy and customize this file for your own use:
```bash
cp examples/sample_toi.yaml my_toi.yaml
# Edit my_toi.yaml with your preferences
```

Then use it with SWP:
```python
from sleepwalker_protocol import SWP

swp = SWP(user_toi_path="my_toi.yaml")
```

## Running All Examples

To run all Python examples:
```bash
for example in examples/*.py; do
    echo "Running $example..."
    python "$example"
    echo "---"
done
```

## Creating Your Own Examples

When creating your own implementations:

1. **Always respect user boundaries** - Check TOI configuration before intervening
2. **Log observations, don't intervene** - SWP detects states but doesn't force processing
3. **Use graduated consent** - Offer support at appropriate levels only
4. **Maintain continuity** - Preserve emotional boundaries across sessions
5. **Privacy first** - Store emotional state data locally only

See the main README for detailed API documentation and integration guides.
