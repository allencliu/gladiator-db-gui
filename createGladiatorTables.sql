-- Create a new table with GladiatorID as the first column
CREATE TABLE IF NOT EXISTS gladiators_new (
    GladiatorID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Age INT,
    BirthYear INT,
    Origin VARCHAR(255),
    Height INT,
    Weight INT,
    Category VARCHAR(255),
    Wins INT,
    Losses INT,
    SpecialSkills VARCHAR(255),
    WeaponOfChoice VARCHAR(255),
    PatronWealth VARCHAR(255),
    EquipmentQuality VARCHAR(255),
    PublicFavor DECIMAL(10, 9),
    InjuryHistory VARCHAR(255),
    MentalResilience VARCHAR(255),
    DietAndNutrition VARCHAR(255),
    TacticalKnowledge VARCHAR(255),
    AllegianceNetwork VARCHAR(255),
    BattleExperience INT,
    PsychologicalProfile VARCHAR(255),
    HealthStatus VARCHAR(255),
    PersonalMotivation VARCHAR(255),
    PreviousOccupation VARCHAR(255),
    TrainingIntensity VARCHAR(255),
    BattleStrategy VARCHAR(255),
    SocialStanding VARCHAR(255),
    CrowdAppealTechniques VARCHAR(255),
    Survived VARCHAR(10)
);

-- Copy data from the existing table to the new table
INSERT INTO gladiators_new
SELECT NULL, Name, Age, BirthYear, Origin, Height, Weight, Category, Wins, Losses, SpecialSkills,
    WeaponOfChoice, PatronWealth, EquipmentQuality, PublicFavor, InjuryHistory,
    MentalResilience, DietAndNutrition, TacticalKnowledge, AllegianceNetwork,
    BattleExperience, PsychologicalProfile, HealthStatus, PersonalMotivation,
    PreviousOccupation, TrainingIntensity, BattleStrategy, SocialStanding,
    CrowdAppealTechniques, Survived
FROM gladiators;

-- Drop the existing table
DROP TABLE gladiators;

-- Rename the new table to the original name
ALTER TABLE gladiators_new RENAME TO gladiators;

-- Display the updated structure of the gladiators table
-- DESCRIBE gladiators;


CREATE TABLE IF NOT EXISTS GladiatorInfo (
    GladiatorID INT PRIMARY KEY,
    Name VARCHAR(255),
    Age INT,
    BirthYear INT,
    Origin VARCHAR(255),
    Height INT,
    Weight INT
);
CREATE TABLE IF NOT EXISTS CombatStats (
    GladiatorID INT PRIMARY KEY,
    FOREIGN KEY (GladiatorID) REFERENCES GladiatorInfo(GladiatorID),-- 
    Category VARCHAR(255),
    Wins INT,
    Losses INT
);
CREATE TABLE IF NOT EXISTS Skills (
    GladiatorID INT PRIMARY KEY,
    FOREIGN KEY (GladiatorID) REFERENCES GladiatorInfo(GladiatorID),
    SpecialSkills VARCHAR(255),
    WeaponOfChoice VARCHAR(255),
    BattleStrategy VARCHAR(255),
    CrowdAppealTechniques VARCHAR(255),
    TacticalKnowledge VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS BackgroundInfo (
    GladiatorID INT PRIMARY KEY,
    FOREIGN KEY (GladiatorID) REFERENCES GladiatorInfo(GladiatorID),
    PreviousOccupation VARCHAR(255),
    TrainingIntensity VARCHAR(255),
    BattleExperience INT,
    PersonalMotivation VARCHAR(255),
    AllegianceNetwork VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS HealthInfo (
    GladiatorID INT PRIMARY KEY,
    FOREIGN KEY (GladiatorID) REFERENCES GladiatorInfo(GladiatorID),
    InjuryHistory VARCHAR(255),
    MentalResilience VARCHAR(255),
    DietAndNutrition VARCHAR(255),
	PsychologicalProfile VARCHAR(255),
    HealthStatus VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS ExternalFactors (
    GladiatorID INT PRIMARY KEY,
    FOREIGN KEY (GladiatorID) REFERENCES GladiatorInfo(GladiatorID),
    EquipmentQuality VARCHAR(255),
    PatronWealth VARCHAR(255),
    PublicFavor DECIMAL(10, 9),
    SocialStanding VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS Outcome (
    GladiatorID INT PRIMARY KEY,
    FOREIGN KEY (GladiatorID) REFERENCES GladiatorInfo(GladiatorID),
    Survived VARCHAR(10)
);


-- Populate GladiatorInfo table
INSERT INTO GladiatorInfo (GladiatorID, Name, Age, BirthYear, Origin, Height, Weight)
SELECT GladiatorID,
 Name, Age, BirthYear, Origin, Height, Weight
FROM gladiators
LIMIT 10000;

-- Populate CombatStats table
INSERT INTO CombatStats (GladiatorID, Category, Wins, Losses)
SELECT GladiatorID, Category, Wins, Losses
FROM gladiators
LIMIT 10000;

-- Populate Skills table
INSERT INTO Skills (GladiatorID, SpecialSkills, WeaponOfChoice, BattleStrategy, CrowdAppealTechniques, TacticalKnowledge)
SELECT GladiatorID, SpecialSkills, WeaponOfChoice, BattleStrategy, CrowdAppealTechniques, TacticalKnowledge
FROM gladiators
LIMIT 10000;

-- Populate BackgroundInfo table
INSERT INTO BackgroundInfo (GladiatorID, PreviousOccupation, TrainingIntensity, BattleExperience, PersonalMotivation, AllegianceNetwork)
SELECT GladiatorID, PreviousOccupation, TrainingIntensity, BattleExperience, PersonalMotivation, AllegianceNetwork
FROM gladiators
LIMIT 10000;

-- Populate HealthInfo table
INSERT INTO HealthInfo (GladiatorID, InjuryHistory, MentalResilience, DietAndNutrition, PsychologicalProfile, HealthStatus)
SELECT GladiatorID, InjuryHistory, MentalResilience, DietAndNutrition, PsychologicalProfile, HealthStatus
FROM gladiators
LIMIT 10000;

-- Populate ExternalFactors table
INSERT INTO ExternalFactors (GladiatorID, EquipmentQuality, PatronWealth, PublicFavor, SocialStanding)
SELECT GladiatorID, EquipmentQuality, PatronWealth, PublicFavor, SocialStanding
FROM gladiators
LIMIT 10000;

-- Populate Outcome table
INSERT INTO Outcome (GladiatorID, Survived)
SELECT GladiatorID, Survived
FROM gladiators
LIMIT 10000;
