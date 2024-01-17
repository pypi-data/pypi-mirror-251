from .yams.yams import Yams
from .config.config import Configurator, EnvironmentType
from .modulator.modulator import Modulator
from pathlib import Path

from .server import create_server


dev_mode: bool = True


def main(config: str = None, path: str = None):
    print("\nApplication started:\n")

    if dev_mode:
        print("Starting configuration...\n")
    config = Configurator(dev_mode=dev_mode)
    
    if dev_mode:
        print("\nConfiguration Complete:\n")

    if dev_mode:
        print("\nParsing Yaml File...\n")
    yaml_file = Yams(config.Config)
    yaml_file.parse_file()
    if dev_mode:
        print("\nParse Complete\n")

    if dev_mode:
        print("\nConfiguring WebService...\n")

    mod_importer = Modulator()
    #! Test to see how import modules works
    for layer_key, layer in yaml_file.Layers.items():
        layer_dir = Path(f"{config.Config.DirectoryPath}/{layer}")

        print(f"Layer: {layer_dir}")
        mod_importer.build_modules_from_dir(layer_dir)

    for key, lam in yaml_file.Lambdas.items():
        parts = lam.Handler.split(".")

        lambda_full_path = Path(
            f"{config.Config.DirectoryPath}/{lam.CodeUri}/{parts[0]}.py"
        )
        
        spec, func = mod_importer.build_modules_from_file(lambda_full_path, lam.FunctionName)

        lam.func = func
        lam.spec = spec
        lam.FullPath = lambda_full_path

    create_server(config.Config, yaml_file.Lambdas, yaml_file.Layers)


if __name__ == "__main__":
    main()
