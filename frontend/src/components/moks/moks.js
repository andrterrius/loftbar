export const FLAVORS = [
    { id: '1', name: 'Double Apple', brand: 'Al Fakher', category: 'Classic', color: '#dc2626' },
    { id: '2', name: 'Mint', brand: 'Tangiers', category: 'Minty', color: '#16a34a' },
    { id: '3', name: 'Mango', brand: 'Darkside', category: 'Fruity', color: '#eab308' },
    { id: '4', name: 'Peach', brand: 'MustHave', category: 'Fruity', color: '#f97316' },
    { id: '5', name: 'Pinkman', brand: 'MustHave', category: 'Berry', color: '#ec4899' },
    { id: '6', name: 'Pineapple', brand: 'Burn', category: 'Tropical', color: '#facc15' },
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
    }
];

export const SETTINGS = {
    basePrice: 20
};

export const TABS = [
    { id: 'flavors', label: 'Вкусы' },
    { id: 'liquids', label: 'Жидкости' },
    { id: 'presets', label: 'Миксы' },
    { id: 'bowls', label: "Чаши"},
    { id: 'settings', label: 'Настройки' },
];

export const PRESET_TABS = ['All', 'Fruity', 'Tropical', 'Classic', 'Minty', 'Berry'];