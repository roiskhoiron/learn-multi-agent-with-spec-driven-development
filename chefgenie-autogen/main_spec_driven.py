import os
import asyncio
import yaml
from agents.spec_aware_coder import SpecAwareCoder
from agents.spec_validator import SpecValidator

async def main():
    specs_dir = "chefgenie-autogen/specs"
    generated_dir = "chefgenie-autogen/generated"
    
    coder = SpecAwareCoder()
    validator = SpecValidator()

    for spec_file in os.listdir(specs_dir):
        if spec_file.endswith(".spec.yaml"):
            print(f"Processing {spec_file}...")
            
            with open(os.path.join(specs_dir, spec_file), 'r') as f:
                spec_content = f.read()
            
            # Generate Code
            print("Generating code...")
            generated_code_raw = await coder.generate_code(spec_content)
            
            # Extract code block
            if "```python" in generated_code_raw:
                generated_code = generated_code_raw.split("```python")[1].split("```")[0].strip()
            elif "```" in generated_code_raw:
                generated_code = generated_code_raw.split("```")[1].split("```")[0].strip()
            else:
                generated_code = generated_code_raw.strip()

            # Validate Code
            print("Validating code...")
            validation_result = await validator.validate(spec_content, generated_code)
            
            if "VALID" in validation_result.upper():
                print(f"Validation successful for {spec_file}!")
                
                # Save generated code
                output_filename = spec_file.replace(".spec.yaml", ".py").replace("-", "_")
                output_path = os.path.join(generated_dir, output_filename)
                
                with open(output_path, 'w') as f:
                    f.write(generated_code)
                print(f"Saved to {output_path}")
            else:
                print(f"Validation failed for {spec_file}:")
                print(validation_result)

if __name__ == "__main__":
    asyncio.run(main())
