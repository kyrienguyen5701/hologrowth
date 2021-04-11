export function GetCSSVar(name: string) {
    return getComputedStyle(document.documentElement).getPropertyValue(name);
}

export function SetCSSVar(name: string, value: string) {
    document.documentElement.style.setProperty(name, value);
}