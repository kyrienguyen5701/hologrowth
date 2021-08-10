import langData from "@/assets/json/localization.json";
import songData from "@/assets/json/songs.json";
import { LanguageData, LocalizationType } from "./interfaces";

export function GetLocalizedText(text: string, localizationType = LocalizationType.Text) {
  let data = {};

  switch (localizationType) {
    case LocalizationType.Text:
      data = langData;
      break;

    case LocalizationType.Song:
      data = songData;
      break;
  
    default:
      data = langData;
      break;
  }

  let lang = localStorage.getItem("lang");
  if (!lang) {
    lang = "en";
    localStorage.setItem("lang", "en");
  }

  let result = "";
  if (Object.keys(data).indexOf(text) != -1) {
    const textData = (data as Record<string, LanguageData>)[text];
    if (Object.keys(textData).indexOf(lang) != -1) {
      switch (lang) {
        case "en":
          result = textData.en || "";
          break;

        case "jp":
          result = textData.jp || "";
          break;
      }
    }
  }

  return result == "" ? text : result;
}

export function GetLocalizedSong(text: string) {
  return GetLocalizedText(text, LocalizationType.Song);
}

export function SetLang(langCode: string) {
  localStorage.setItem("lang", langCode);
  console.log(`Set language: ${langCode}`);
}
