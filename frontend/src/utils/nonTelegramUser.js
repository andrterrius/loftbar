let cachedProfile = null;

export function setNonTelegramUserProfile(profile) {
    cachedProfile = profile;
}

export function getNonTelegramUserProfile() {
    return cachedProfile;
}
