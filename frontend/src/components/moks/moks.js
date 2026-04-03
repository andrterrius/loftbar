export const FLAVORS = [
    { id: '1', name: 'Double Apple', brand: 'Al Fakher', categories: [{'name': 'Classic', 'id': '1'}], color: '#dc2626' },
    { id: '2', name: 'Mint', brand: 'Tangiers', categories: [{'name': 'Minty', 'id': '2'}], color: '#16a34a' },
    { id: '3', name: 'Mango', brand: 'Darkside', categories: [{'name': 'Minty', 'id': '2'}, {'name': 'Fruity', 'id': '3'}], color: '#eab308' },
    { id: '4', name: 'Peach', brand: 'MustHave', categories: [{'name': 'Fruity', 'id': '3'}], color: '#f97316' },
    { id: '5', name: 'Pinkman', brand: 'MustHave', categories: [{'name': 'Berry', 'id': '4'}], color: '#ec4899' },
    { id: '6', name: 'Pineapple', brand: 'Burn', categories: [{'name': 'Tropical', 'id': '4'}], color: '#facc15' },
];

export const FLAVORS_CATEGORIES = [
    { id: '3', name: 'Fruity'},
    { id: '2', name: 'Minty'}
];

export const BOWL_OPTIONS = [
    { type: 'Classic',    icon: '🏺', isFruit: false, price: 0  },
    { type: 'Silicon',    icon: '⚫', isFruit: false, price: 20  },
    { type: 'Grapefruit', icon: '🍊', isFruit: true,  price: 30  },
    { type: 'Lemon',      icon: '🍋', isFruit: true,  price: 40  },
    { type: 'Orange',     icon: '🍊', isFruit: true,  price: 50  },
    { type: 'Coconut',    icon: '🥥', isFruit: true,  price: 60  },
    { type: 'Pineapple',  icon: '🍍', isFruit: true,  price: 70  },
    { type: 'Pitahaya',   icon: '🐉', isFruit: true,  price: 80 },
    { type: 'Watermelon', icon: '🍉', isFruit: true,  price: 90  },
];

export const LIQUIDS = [
    { id: 'water', name: 'Water', description: 'Обычная вода' },
    { id: 'milk', name: 'Milk', description: 'Молоко' },
    { id: 'green_tea', name: 'Green Tea', description: 'Зелёный чай' },
    { id: 'juice', name: 'Juice', description: 'Сок' },
];

export const PRESETS = [
    {
        id: '1',
        name: 'Apple Freeze',
        category: 'Fruity',
        description: 'A refreshing blend of sweet double apple and icy mint.',
        imageUrl: null,
        price: 150,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[0], percent: 70 },
            { flavor: FLAVORS[1], percent: 30 }
        ],
        bowl: { icon: BOWL_OPTIONS[0].icon, name: BOWL_OPTIONS[0].type }
    },
    {
        id: '2',
        name: 'Double Apple',
        category: 'Tropical',
        description: 'Summer vibes with a sweet mango base.',
        imageUrl: null,
        price: 180,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[2], percent: 80 },
            { flavor: FLAVORS[1], percent: 20 }
        ],
        bowl: { icon: BOWL_OPTIONS[2].icon, name: BOWL_OPTIONS[2].type }
    },
    {
        id: '3',
        name: 'Double Apple',
        category: 'Tropical',
        description: 'Summer vibes with a sweet mango base.',
        imageUrl: null,
        price: 180,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[2], percent: 80 },
            { flavor: FLAVORS[1], percent: 20 }
        ],
        bowl: { icon: BOWL_OPTIONS[2].icon, name: BOWL_OPTIONS[2].type }
    },
    {
        id: '4',
        name: 'Double Apple',
        category: 'Tropical',
        description: 'Summer vibes with a sweet mango base.',
        imageUrl: null,
        price: 180,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[2], percent: 80 },
            { flavor: FLAVORS[1], percent: 20 }
        ],
        bowl: { icon: BOWL_OPTIONS[2].icon, name: BOWL_OPTIONS[2].type }
    },
    {
        id: '5',
        name: 'Double Apple',
        category: 'Tropical',
        description: 'Summer vibes with a sweet mango base.',
        imageUrl: null,
        price: 180,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[2], percent: 80 },
            { flavor: FLAVORS[1], percent: 20 }
        ],
        bowl: { icon: BOWL_OPTIONS[2].icon, name: BOWL_OPTIONS[2].type }
    },
    {
        id: '6',
        name: 'Double Apple',
        category: 'Tropical',
        description: 'Summer vibes with a sweet mango base.',
        imageUrl: null,
        price: 180,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[2], percent: 80 },
            { flavor: FLAVORS[1], percent: 20 }
        ],
        bowl: { icon: BOWL_OPTIONS[2].icon, name: BOWL_OPTIONS[2].type }
    },
    {
        id: '7',
        name: 'Double Apple',
        category: 'Tropical',
        description: 'Summer vibes with a sweet mango base.',
        imageUrl: null,
        price: 180,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[2], percent: 80 },
            { flavor: FLAVORS[1], percent: 20 }
        ],
        bowl: { icon: BOWL_OPTIONS[2].icon, name: BOWL_OPTIONS[2].type }
    },
    {
        id: '8',
        name: 'Double Apple',
        category: 'Tropical',
        description: 'Summer vibes with a sweet mango base.',
        imageUrl: null,
        price: 180,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[2], percent: 80 },
            { flavor: FLAVORS[1], percent: 20 }
        ],
        bowl: { icon: BOWL_OPTIONS[2].icon, name: BOWL_OPTIONS[2].type }
    },
    {
        id: '9',
        name: 'Double Apple',
        category: 'Tropical',
        description: 'Summer vibes with a sweet mango base.',
        imageUrl: null,
        price: 180,
        liquid: { id: 'water', name: 'Water', hex_color: '#06b6d4' },
        flavors: [
            { flavor: FLAVORS[2], percent: 80 },
            { flavor: FLAVORS[1], percent: 20 }
        ],
        bowl: { icon: BOWL_OPTIONS[2].icon, name: BOWL_OPTIONS[2].type }
    }
];

export const SETTINGS = {
    basePrice: 20,
    addedStrengthPrice: 5
};

export const TABS = [
    { id: 'flavors', label: 'Вкусы' },
    { id: 'liquids', label: 'Жидкости' },
    { id: 'presets', label: 'Миксы' },
    { id: 'bowls', label: "Чаши"},
    { id: 'settings', label: 'Настройки' },
];

export const PRESET_TABS = ['All', 'Fruity', 'Tropical', 'Classic', 'Minty', 'Berry'];