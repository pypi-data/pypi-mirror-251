SKILLS = [
    {
        "Dungeoneering": (
            "Navigate dungeons and caves, detect grades and slopes, "
            "identify subterranean creatures."
        ),
    },
    {
        "Fast-Talk": "Convince another through charisma or subterfuge.",
    },
    {
        "Hypermnesia": "Perfectly recall information the character was previously exposed to.",
    },
    {
        "Intuition": "Discern lies or malicious intent; notice an important detail.",
    },
    {
        "Knowledge": (
            "Awareness of a bit of lore, science, or trivia that may be relevant to the situation."
        ),
    },
    {
        "Legerdemain": "Performing card tricks, picking pockets, and similar.",
    },
    {
        "Muscle": "Break down doors, lift heavy things, etc.",
    },
    {
        "Parkour": "Balancing, climbing, jumping, tumbling.",
    },
    {
        "Sneak": "Quietly move or hide without being noticed.",
    },
    {
        "Survival": (
            "Navigate, find food and shelter, track animals and people while in the wilderness."
        ),
    },
    {
        "Tinkering": (
            "Pick locks, set or disarm traps, discern how technological items work. "
            "Tools may be required."
        ),
    },
    {
        "Zoophilism": "Ability to calm, empathize with, and communicate in a "
        "rudimentary fashion with animals."
    },
]

EXTRAORDINARY_ABILITIES = [
    {
        "Alchemy": (
            "Mix potions and poisons, provided the necessary ingredients are at hand. "
            "Identify unknown liquids with a successful check."
        ),
    },
    {
        "Beastmaster": (
            "Make a check to tame a beast who's hit points don't exceed your own. "
            "The pet must be fed and treated well. If ever neglected, or called on to "
            "aid in direct combat, another check must be made to prevent the creature from "
            "abandoning you. If this ability is taken a second time, or you have the "
            "zoophilism skill, the checks are successful on 4+."
        ),
    },
    {
        "Berserks Mode": (
            "You may choose to enter a berserker rage, which lasts until the end of a "
            "combat. All attacks are made with disadvantage, but deal double damage on a hit."
        ),
    },
    {
        "Cantraps": "Produce minor, non-damaging magical effects at will.",
    },
    {
        "Diehard": (
            "The first time you fall to 0 hit points in a given day, you immediately gain "
            "1 hit point back and don't lose consciousness."
        ),
    },
    {
        "Healing": (
            "As an action, you can make a check to heal an ally other than yourself. "
            "On a success, the target creature is healed for 2 hit points. Alternatively, "
            "this ability can also be used to cure poison, disease, and other physical "
            "ailments that are non-magical. You must touch the recipient to perform the healing."
        ),
    },
    {
        "Read Magic": (
            "Ability to discern arcane writing and cast spells from scrolls. When this ability "
            "is gained, the character also gains two randomly determined scrolls (see Magic)."
        ),
    },
    {
        "Repel Undead": (
            "On a successful check, you add the total of the two dice and turn away that many "
            "hit points of undead creatures. May be attempted once per combat."
        ),
    },
    {
        "Vigilant": (
            "Whenever your side loses initiative, make a check. If the check is successful, "
            "you act first."
        ),
    },
    {
        "Wizardry": (
            "Knowledge of and ability to cast three randomly determined spells (see Magic). "
            "This ability may be taken multiple times, and three additional random spells "
            "are learned each time."
        ),
    },
    {
        "Perceptive": (
            "You have a chance to notice secret doors or other important yet subtle clues "
            "that others would miss. The GM needs to make the checks for this, and may need "
            "to be reminded from time to time that you have this ability."
        ),
    },
    {
        "Weapon Training": "You make combat checks with skill for a specific weapon group.",
    },
]

# Backgrounds from Knave, with some modifications
BACKGROUNDS = [
    "Academic",
    "Beggar",
    "Butcher",
    "Burglar",
    "Charlatan",
    "Cook",
    "Cultist",
    "Farmer",
    "Gambler",
    "Herbalist",
    "Mariner",
    "Mercenary",
    "Merchant",
    "Outlaw",
    "Performer",
    "Pickpocket",
    "Smuggler",
    "Tracker",
]

BASE_EQUIPMENT = [
    "Rucksack",
    "Rations (7)",
    "Waterskin",
    "Flint & Steel",
    "Torches (6)",
]

CLOTHING_ITEMS = [
    "Helmet",
    "Fine Cape",
    "Stylish Hat",
    "Hooded Woolen Cloak",
    "Eye Patch",
    "Bandit Mask",
]

EQUIPMENT_A = [
    "Lasso",
    "Flask of Acid",
    "Pouch of Marbles",
    "Ball of Twine (100')",
    "Flask of Oil (2)",
    "Molotov Cocktail",
]

EQUIPMENT_B = [
    "Prybar",
    "Whistle",
    "Skeleton Key",
    "Hammer, 10 Pitons",
    "Spyglass",
    "Lock Picks",
]

EQUIPMENT_C = [
    "10' Pole",
    "Pouch of Sand",
    "Compass",
    "Jar of Lard",
    "Pliers",
    "Rope (50')",
]

LIGHT_MELEE_WEAPONS = [
    "Dagger",
    "Stiletto",
    "Hand Axe",
    "Mace",
    "Nunchaku",
    "Sword",
    "Quarterstaff",
]

HEAVY_MELEE_WEAPONS = [
    "Battle Axe",
    "Double-Bladed Scimitar",
    "Bat'leth",
    "Greatclub",
    "Glaive",
    "Halberd",
    "Polearm",
    "Maul",
    "Zweihänder",
]

RANGED_WEAPONS = [
    "Crossbow, boltcase of 12 Bolts",
    "Bow, quiver of 12 Arrows",
    "Darts, bandolier of 12",
    "Javelins, sheaf of 6",
    "Shuriken, bandolier of 12",
    "Sling, pouch of 12 Stones",
]

# A fork of Knave spells, customized for d666
SPELLS = {
    "Adhere": "Object is covered in extremely sticky slime.",
    "Animate Object": "Object obeys your commands as best it can. It can walk 15ft per round.",
    "Anthropomorphize": "A touched animal either gains human intelligence or human appearance for L days.",
    "Arcane Eye": "You can see through a magical floating eyeball that flies around at your command.",
    "Astral Prison": "An object is frozen in time and space within an invulnerable crystal shell.",
    "Attract": "L+1 objects are strongly magnetically attracted to each other if they come within 10 feet.",
    "Auditory Illusion": "You create illusory sounds that seem to come from a direction of your choice.",
    "Babble": "A creature must loudly and clearly repeat everything you think. It is otherwise mute.",
    "Beast Form": "You and your possessions transform into a mundane animal.",
    "Befuddle": "L creatures of your choice are unable to form new short term memories for the duration of the spell.",
    "Bend Fate": "Roll L+1 dice. Whenever you must roll a die after casting the spell, you must choose and then discard one of the rolled results until they are all gone.",
    "Bird Person": "Your arms turn into huge bird wings.",
    "Body Swap": "You switch bodies with a creature you touch . If one body dies, the other dies as well.",
    "Catherine": "A woman wearing a blue dress appears until end of spell. She will obey polite, safe requests.",
    "Charm": "L creatures treat you like a friend.",
    "Command": "A creature obeys a single, three word command that does not harm it.",
    "Comprehend": "You become fluent in all languages.",
    "Control Plants": "Nearby plants and trees obey you and gain the ability to move at 5 feet per round.",
    "Control Weather": "You may alter the type of weather at will, but you do not otherwise control it.",
    "Counterspell": "Make a check against the caster of a nearby spell. You may do this out of turn as a reaction, or against an ongoing magical effect. On a success, you may cancel the spell.",
    "Deafen": "All nearby creatures are deafened.",
    "Detect Magic": "You hear nearby magical auras singing. Volume and harmony signify the aura’s power and refinement.",
    "Disassemble": "Any of your body parts may be detached and reattached at will, without causing pain or damage. You can still control them.",
    "Disguise": "You may alter the appearance of L characters at will as long as they remain humanoid. Attempts to duplicate other characters will seem uncanny.",
    "Displace": "An object appears to be up to L×10ft from its actual position",
    "Earthquake": "The ground begins shaking violently. Structures may be damaged or collapse.",
    "Elasticity": "Your body can stretch up to L×10ft",
    "Elemental Wall": "A straight wall of ice or fire L×40ft long and 10ft high rises from the ground.",
    "Filch": "L visible items teleport to your hands.",
    "Fog Cloud": "Dense fog spreads out from you.",
    "Frenzy": "L creatures erupt in a frenzy of violence.",
    "Gate": "A portal to a random plane opens.",
    "Gravity Shift": "You can change the direction of gravity (for yourself only) up to once per round.",
    "Greed": "L creatures develop an overwhelming urge to possess a visible item of your choice.",
    "Haste": "Your movement speed is tripled.",
    "Hatred": "L creatures develop a deep hatred of another creature or group of creatures and wish to destroy it.",
    "Hear Whispers": "You can hear faint sounds clearly.",
    "Hover": "An object hovers, frictionless, 2ft above the ground. It can hold up to L humanoids.",
    "Hypnotize": "A creature enters a trance and will truthfully answer L yes or no questions you ask it.",
    "Icy Touch": "A thick ice layer spreads across a touched surface, up to L×10ft in radius.",
    "Illuminate": "A floating light moves as you command.",
    "Increase Gravity": "The gravity in an area triples.",
    "Invisible Tether": "Two objects within 10ft of each other cannot be moved more than 10ft apart.",
    "Knock": "L nearby mundane or magical locks unlock.",
    "Leap": "You can jump up to L×10ft in the air.",
    "Liquid Air": "The air around you becomes swimmable.",
    "Magic Dampener": "All nearby magical effects have their effectiveness halved.",
    "Manse": "A sturdy, furnished cottage appears for L×12 hours. You can permit and forbid entry to it at will.",
    "Marble Madness": "Your pockets are full of marbles, and will refill every round.",
    "Masquerade": "L characters’ appearances and voices become identical to a touched character",
    "Miniaturize": "You and L other touched creatures are reduced to the size of a mouse.",
    "Mirror Image": "L illusory duplicates of yourself appear under your control.",
    "Mirrorwalk": "A mirror becomes a gateway to another mirror that you looked into today.",
    "Multiarm": "You gain L extra arms.",
    "Night Sphere": "A n L×40ft wide sphere of darkness displaying the night sky appears.",
    "Objectify": "You become any inanimate object between the size of a grand piano and an apple.",
    "Ooze Form": "You become a living jelly.",
    "Pacify": "L creatures have an aversion to violence.",
    "Phantom Coach": "A ghostly coach appears until end of spell. It moves unnaturally fast over any terrain, including water.",
    "Phobia": "L creatures become terrified of an object of your choice.",
    "Pit": "A pit 10ft wide and L×5 ft deep opens in the ground.",
    "Primeval Surge": "An object grows to the size of an elephant. If it is an animal, it is enraged.",
    "Psychometry": "The referee answers L yes or no questions about a touched object.",
    "Pull": "An object of any size is pulled directly towards you with the strength of L men for one round.",
    "Push": "An object of any size is pushed directly away from you with the strength of L men for one round.",
    "Raise Dead": "L skeletons rise from the ground to serve you. They are incredibly stupid and can only obey simple orders.",
    "Raise Spirit": "The spirit of a dead body manifests and will answer L questions.",
    "Read Mind": "You can hear the surface thoughts of nearby creatures.",
    "Repel": "L+1 objects are strongly magnetically repelled from each other if they come within 10 feet.",
    "Scry": "You can see through the eyes of a creature you touched earlier today",
    "Sculpt Elements": "All inanimate material behaves like clay in your hands.",
    "Shroud": "L creatures are invisible until they move.",
    "Shuffle": "L creatures instantly switch places. Determine where they end up randomly.",
    "Sleep": "L creatures fall into a light sleep.",
    "Smoke Form": "Your body becomes living smoke.",
    "Snail Knight": "10 minutes after casting, a knight sitting astride a giant snail rides into view. He is able to answer most questions related to quests and chivalry, and may aid you if he finds you worthy.",
    "Sniff": "You can smell even the faintest traces of scents.",
    "Sort": "Inanimate items sort themselves according to categories you set. The categories must be visually verifiable.",
    "Spectacle": "A clearly unreal but impressive illusion of your choice appears, under your control. It may be up to the size of a palace and has full motion and sound.",
    "Spellseize": "Cast this as a reaction to another spell going off to make a temporary copy of it that you can cast at any time before this spell ends.",
    "Spider Climb": "You can climb surfaces like a spider.",
    "Summon Cube": "Once per second, (6 times per round) you may summon or banish a 3 foot wide cube of earth. New cubes must be affixed to the earth or to other cubes.",
    "Swarm": "You become a swarm of crows, rats, or piranhas. You only take damage from area effects.",
    "Telekinesis": "You may mentally move L items.",
    "Telepathy": "L+1 creatures can hear each other's thoughts, no matter how far apart they move.",
    "Teleport": "An object disappears and reappears on the ground in a visible, clear area up to L×40ft away.",
    "Thaumaturgic Anchor": "Object becomes the target of every spell cast near it.",
    "Thicket": "A thicket of trees and dense brush up to L×40ft wide suddenly sprouts up.",
    "Time Jump": "An object disappears as it jumps L×10 minutes into the future. When it returns, it appears in the unoccupied area nearest to where it left.",
    "Summon Idol": "A carved stone statue the size of a four poster bed rises from the ground.",
    "Time Rush": "Time in a 40ft bubble starts moving 10 times faster.",
    "Time Slow": "Time in a 40ft bubble slows to 10%.",
    "True Sight": "You see through all nearby illusions.",
    "Upwell": "A spring of seawater appears.",
    "Vision": "You completely control what a creature sees.",
    "Visual Illusion": "A silent, immobile, illusion of your choice appears, up to the size of a bedroom.",
    "Ward": "A silver circle 40ft across appears on the ground. Choose one thing that cannot cross it: Living creatures, dead creatures, projectiles or metal.",
    "Web": "Your wrists can shoot thick webbing.",
    "Wizard Mark": "Your finger can shoot a stream of ulfire colored paint. This paint is only visible to you, and can be seen at any distance, even through solid objects.",
    "X Ray Vision": "You gain X Ray vision.",
}
