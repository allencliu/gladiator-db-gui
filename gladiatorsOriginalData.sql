CREATE TABLE gladiators (
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

-- Create a new table with GladiatorID as the first column
CREATE TABLE gladiators_new (
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
DESCRIBE gladiators;
