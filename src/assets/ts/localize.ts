import langData from "@/assets/json/localization.json";
import songData from "@/assets/json/songs.json";
import { LanguageData, LocalizationType, MonthAbbrv } from "./interfaces";

export function GetLocalizedText(
  text: string,
  localizationType = LocalizationType.Text
) {
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

  return result === "" && text !== "space" ? text : result;
}

export function GetLocalizedSong(text: string) {
  return GetLocalizedText(text, LocalizationType.Song);
}

export function SetLang(langCode: string) {
  localStorage.setItem("lang", langCode);
  console.log(`Set language: ${langCode}`);
}

export function GetLocalizedDate(dateString: string) {
  let lang = localStorage.getItem("lang");
  if (!lang) {
    lang = "en";
    localStorage.setItem("lang", "en");
  }
  if (lang === "en") {
    return dateString;
  }
  // birthday case
  if (dateString.includes(" ")) {
    const components = dateString.split(" ");
    const day = parseInt(components[0], 10);
    const month = (components[1].slice(0, 3) as unknown) as MonthAbbrv;
    let result = `${MonthAbbrv[month] + 1}月 ${day}日`;
    if (components.length === 3) {
      const year = components[2];
      result = `${year}年 ${result};`;
    }
    return result;
  }
  // debut day case
  if (dateString.includes("/")) {
    const components = dateString.split("/");
    const year = components[0];
    const month = components[1];
    const day = components[2];
    const result = `${year}年 ${month}月 ${day}日`;
    return result;
  }
}

export function GetChartLocalizedDate(dateString: string) {
  let lang = localStorage.getItem("lang");
  if (!lang) {
    lang = "en";
    localStorage.setItem("lang", "en");
  }
  if (lang === "en") {
    return dateString;
  }
  const components = dateString.split(" ");
  const month = MonthAbbrv[(components[0] as unknown) as MonthAbbrv] + 1;
  let result =
    components[1].length === 2
      ? `${month}月 ${parseInt(components[1], 10)}日`
      : `${components[1]}年 ${month}月`;
  if (components.length === 3) {
    const year = components[2];
    result = `${year}年 ${result}`;
  }
  return result;
}
