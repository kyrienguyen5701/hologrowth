import langData from "@/assets/json/localization.json";
import { LanguageData } from "./interfaces";
let lang = "en";

export function GetLocalizedText(text :string)
{
    if (Object.keys(langData).indexOf(text) != -1)
    {
        const textData = (langData as Record<string, LanguageData>)[text];
        if (Object.keys(textData).indexOf(lang) != -1)
        {
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

export function SetLang(langName: string)
{
    lang = langName;
}