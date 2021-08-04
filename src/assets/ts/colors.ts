import { GetCSSVar, SetCSSVar } from "./common";

export const COLOR_VARS = [
  "",
  "-tint-25",
  "-tint-50",
  "-shade-25",
  "-shade-50",
  "-complement"
];

export function ChangeColor(member: string) {
  if (member == "Ina'nis") member = "Inanis"
  COLOR_VARS.forEach(colorVar => {
    const name = `--color-${member}${colorVar}`;
    const targetName = `--color-current${colorVar}`;
    SetCSSVar(targetName, GetCSSVar(name));
  });
}