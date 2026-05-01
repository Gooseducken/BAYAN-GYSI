import os
import sys

# Полный список устаревших и отсутствующих прототипов из твоих логов
PROTOTYPES_TO_REMOVE = {
    "DefaultStationBeaconCorpsman", "DefaultStationBeaconMailroom", "DefaultStationBeaconMetempsychosis",
    "DrinkJuiceOrangeJuicebox", "EpistemicsTechFab", "FoodMothToastedSeeds", "GavelBlock", "GlimmerProber",
    "GunSafeSniperGrand", "HatSpawner", "HolopadEpistemicsMantis", "HolopadJusticeProsecutor",
    "HolopadSecurityCorpsman", "HolopadSecurityPermaKitchen", "HolopadSecurityPermaWorkshop",
    "HoloprojectorEngineering", "KitchenDeepFryer", "LauncherSyringe", "LawSpawner",
    "LockerAdministrativeAssistantFilled", "LockerChiefJusticeFilled", "LockerClerkFilled",
    "LockerForensicMantisFilled", "LockerParamedicFilledHardsuit", "LockerQuarterMasterFilledHardsuit",
    "LockerSurgeonFilled", "LogisticsTechFab", "MiniSyringe", "Oracle", "PillMindbreakerToxin",
    "PosterLegitSafetyMothPills", "PoweredLightBlueInterior", "PoweredLightColoredFrostyBlue",
    "PoweredLightColoredRed", "PoweredSmallLightMaintenance", "RandomAnimalSpawner", "RandomBoards",
    "RandomBook", "RandomWoodenStructure", "ReverseEngineeringMachine", "RifleSafeSpawner", "Roboisseur",
    "SecBreachingHammer", "SecureCabinetCommand", "SentientSmileCore", "SignDirectionaCourt",
    "SignDirectionalLogistics", "SignDirectionalMail", "SignSec", "SophicScribe", "SpareIdCabinetFilled",
    "SpawnMobSecLaikaOrShiva", "SpawnPointAdminAssistant", "SpawnPointCargoAssistant", "SpawnPointChiefJustice",
    "SpawnPointClerk", "SpawnPointCourier", "SpawnPointForensicMantis", "SpawnPointLocationMidRoundAntag",
    "SpawnPointProsecutor", "SpawnPointSurgeon", "SuitStorageCorpsman", "SuitStorageSecDeltaV",
    "SuperweaponSafeSpawner", "TrialTimer", "VendingMachineCourierDrobe", "VendingMachineMNKDrobe",
    "VendingMachineRepDrobe", "WarpPointArrivals", "WarpPointAtmos", "WarpPointBotany", "WarpPointChapel",
    "WarpPointCryo", "WarpPointDisposals", "WarpPointDorms", "WarpPointEngineering", "WarpPointEpistemics",
    "WarpPointEvac", "WarpPointHOP", "WarpPointJanitor", "WarpPointKitchen", "WarpPointLogistics",
    "WarpPointMedical", "WarpPointSalvage", "WarpPointSecurity", "WarpPointVault", "WeaponRevolverSnub",
    "WeaponShotgunKammererNonLethal", "WeaponTurretAI", "WindoorMailLocked", "WindoorSecureClerkLocked"
}

def clean_ss14_map(filename: str):
    # Определяем путь к папке, где лежит скрипт
    try:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    except Exception:
        base_path = os.getcwd()
        
    input_path = os.path.join(base_path, filename)
    output_path = os.path.join(base_path, f"cleaned_{filename}")

    print(f"--- ДИАГНОСТИКА ---")
    print(f"Папка: {base_path}")
    if os.path.exists(input_path):
        print(f"Файл '{filename}' найден. Начинаю очистку...")
    else:
        print(f"ОШИБКА: Файл '{filename}' не найден в папке.")
        print(f"Содержимое папки: {os.listdir(base_path)}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    current_block = []
    is_skipping = False

    for line in lines:
        stripped = line.strip()
        
        # Проверяем начало блока по тире перед proto
        if stripped.startswith('- proto:'):
            # Сохраняем предыдущий блок, если он был валидным
            if current_block and not is_skipping:
                cleaned_lines.extend(current_block)
            
            current_block = [line]
            # Извлекаем название прототипа (убираем '- proto:', кавычки и пробелы)
            proto_name = stripped.replace('- proto:', '').strip().strip('"\'')
            
            # Если прототип в списке плохих — помечаем блок на удаление
            is_skipping = proto_name in PROTOTYPES_TO_REMOVE
        
        elif current_block:
            # Продолжаем собирать строки текущего блока (entities, компоненты и т.д.)
            current_block.append(line)
        else:
            # Это строки до начала первого блока сущностей (метаданные карты)
            cleaned_lines.append(line)

    # Не забываем про последний блок в файле
    if current_block and not is_skipping:
        cleaned_lines.extend(current_block)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    print(f"-------------------")
    print(f"ГОТОВО! Очищенный файл: cleaned_{filename}")

if __name__ == "__main__":
    # Укажи здесь точное название своего файла
    clean_ss14_map("map.yml")