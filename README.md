# Program na Sledovanie Čiary

Tento repozitár obsahuje program na sledovanie čiary s testovanými komponentmi organizovanými v štruktúrovanej forme. Repozitár je rozdelený do dvoch hlavných adresárov:

1. `testFiles`
2. `algorithms`

## Štruktúra Adresárov

### 1. `testFiles`

Tento adresár je určený na testovanie jednotlivých komponentov programu na sledovanie čiary. Obsahuje tri podadresáre:

#### `MotorTest`
- **Popis:** Obsahuje test pre funkčnosť motorov.
- **Obsah:**
  - `Motor_Test.py`: Skript na testovanie motorového komponentu.

#### `CameraTest`
- **Popis:** Obsahuje test pre funkčnosť kamery.
- **Obsah:**
  - `Camera_Test.py`: Skript na testovanie kamerového komponentu.
  - `test_Pictures/`: Adresár obsahujúci testovacie obrázky použité pre testovanie kamery.
  - `test_Pictures/output/`: Adresár, kde sa ukladajú výstupy testov.

#### `IRTest`
- **Popis:** Obsahuje test pre funkčnosť IR senzora.
- **Obsah:**
  - `IR_Test.py`: Skript na testovanie IR senzora.

### 2. `algorithms`

Tento adresár obsahuje samotné algoritmy na sledovanie čiary, implementované buď pomocou kamery alebo IR senzora.

#### `Camera_Follow_Line.py`
- **Popis:** Program na sledovanie čiary pomocou kamery.
- **Použitie:** 
  ```bash
  python Camera_Follow_Line.py
  ```

#### `IR_Follow_Line.py`
- **Popis:** Program na sledovanie čiary pomocou IR senzorov.
- **Použitie:**
  ```bash
  python IR_Follow_Line.py
  ```

## Testovanie Komponentov

### Test Motorov

Prejdite do adresára `MotorTest` a spustite testovací skript:

```bash
cd testFiles/MotorTest
python Motor_Test.py
```
Testovací skript funguje nasledovne:

- Každý motor je individuálne napájaný dopredu na jednu sekundu, potom dozadu na jednu sekundu. 
- Každý motor je napájaný dopredu na jednu sekundu s 40% výkonom, potom je napájaný dopredu na jednu sekundu s 80% výkonom.
- Každý motor je napájaný, ale nie rovnakým smerom.

Ak sa všetky tri fázy testu vykonajú správne, motory fungujú správne.

### Test Kamery

Prejdite do adresára `camera_test` a spustite testovací skript:

```bash
cd test_dir/camera_test
python test.py
```

Testovací skript funguje nasledovne:

- V prvej fáze program spracováva vopred pripravený obrázok, na ktorom filtruje čiaru a nájde jej ťažisko.
- V druhej fáze program spracováva živý obraz zachytený kamerou, na ktorom filtruje čiaru a nájde jej ťažisko.
- Z prvej fázy do druhej prejdete stlačením klávesy q.
- Z druhej fázy ukončíte program stlačením klávesy q.

Testovací skript používa obrázky z adresára `test_pictures` a výstupy ukladá do adresára `output`.

### Test IR Senzora

Prejdite do adresára `IRTest` a spustite testovací skript:

```bash
cd testFiles/IRTest
python IR_Test.py
```

Testovací skript funguje nasledovne:

- Program nekonečne meria dáta z troch pripojených senzorov a tieto dáta vypisuje.
- Program môžete zastaviť kombináciou kláves Ctrl+C.

## Spustenie Programov na Sledovanie Čiary

### Program na Sledovanie Čiary Pomocou Kamery

Prejdite do adresára `algorithms` a spustite program na sledovanie čiary pomocou kamery:

```bash
cd algorithms
python camera_line_follower.py
```

### Program na Sledovanie Čiary Pomocou IR Senzorov

Prejdite do adresára `algorithms` a spustite program na sledovanie čiary pomocou IR senzorov:

```bash
cd algorithms
python ir_line_follower.py
```

## Dodatočné Informácie

Uistite sa, že máte nainštalované všetky závislosti pred spustením testov a programov. Závislosti môžete typicky nainštalovať pomocou:

```bash
pip install -r requirements.txt
```

## Autor

- **Jozef Nyitrai** - [juszuf69](https://github.com/juszuf69)

## GitHub Repozitár

- **Repozitár:** [Jozef_Nyitrai_BP](https://github.com/juszuf69/Jozef_Nyitrai_BP)