import importlib

def MultiImport(ModulesToImport: list[str]) -> dict:
    ImportedModulesDict: dict = {}
    
    for name in ModulesToImport:
        ImportedModulesDict[name] = importlib.import_module(name)

    return ImportedModulesDict

def DisplayAllPackagesImported(AllModules: dict) -> None:
    for key in AllModules:
        print(f"{key}")