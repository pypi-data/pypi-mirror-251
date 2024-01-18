from MainFuncs import *

AllModules = MultiImport([
    "cython",
    "pyautogui",
    "requests",
])

requests = AllModules["requests"]

#print(requests.get("https://google.com").text)

DisplayAllPackagesImported(AllModules)