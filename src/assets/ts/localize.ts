import langData from "@/assets/json/localization.json";
import { LanguageData } from "./interfaces";

export function GetLocalizedText(text: string) {
  let lang = localStorage.getItem("lang");
  if (!lang) {
    lang = "en";
    localStorage.setItem("lang", "en");
  }
  if (Object.keys(langData).indexOf(text) != -1) {
    const textData = (langData as Record<string, LanguageData>)[text];
    if (Object.keys(textData).indexOf(lang) != -1) {
      switch (lang) {
        case "en":
          return textData.en || "";

        case "jp":
          return textData.jp || "";
      }
    }
    return text;
  }
  return text;
}

export function SetLang(langCode: string) {
  localStorage.setItem("lang", langCode);
  console.log(`Set language: ${langCode}`);
}
