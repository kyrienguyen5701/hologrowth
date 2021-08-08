import * as interfaces from "./interfaces";
import { format } from "date-fns";

export function GetCSSVar(name: string) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

export function SetCSSVar(name: string, value: string) {
  document.documentElement.style.setProperty(name, value);
}

export function GetYoutubeURL(channelId: string) {
  return "https://youtube.com/" + channelId;
}

export function GetProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

export function ContainsKey(obj: Record<string, any>, searchKey: string): boolean {
  return Object.keys(obj).includes(searchKey);
}

export function Categorize(
  data: interfaces.TalentData[],
  type: interfaces.DataType
): interfaces.Dictionary<interfaces.TalentData[]> {
  const result = {} as interfaces.Dictionary<interfaces.TalentData[]>;
  let findKey = "" as keyof interfaces.TalentData;
  switch (type) {
    case interfaces.DataType.Branch:
      findKey = "branch";
      break;

    case interfaces.DataType.GenName:
      findKey = "genName";
      break;

    case interfaces.DataType.GenNumber:
      findKey = "genNumber";
      break;

    case interfaces.DataType.GenOther:
      findKey = "genOther";
      break;

    case interfaces.DataType.Name:
      findKey = "name";
      break;

    case interfaces.DataType.ChannelId:
      findKey = "channelId";
      break;

    default:
      break;
  }

  for (let i = 0; i < data.length; i++) {
    const key = GetProperty(data[i], findKey) as string;
    // if (!data[i].ContainsKey(key)) {
    if (!ContainsKey(result, key)) {
      result[key] = [data[i]];
    } else {
      result[key].push(data[i]);
    }
  }

  return result;
}

export function GetTalentName(name: string)
{
  const s = name.split("-")
  for (let i = 0; i < s.length; i++)
  {
    s[i] = s[i].charAt(0).toUpperCase() + s[i].substring(1);
  }
  return s.join(" ")
}

export function GetTalentCSSName(name: string)
{
  const s = name.replace(/ /g, "-");
  const _ = s.split("-");
  const result = _[_.length - 1];
  switch (result)
  {
    case "Ina'nis":
      return "Inanis";
  }
  return result;
}

export const countFormatter = (count: number) => {
  if (count == undefined) return "";
  const thousand = 1000;
  const million = 1000000;
  if (count < thousand) return count;
  if (count < million) return `${count / thousand}K`;
  return `${count / million}M`;
};

export const dateFormatter = (val: string) => {
  return format(new Date(val), "MMM dd");
};

export const availableRangesMap = (range: number) => {
  switch (range) {
    case 7:
      return "Last Week";
    case 30:
      return "Last Month";
    case 365:
      return "Last Year";
    case 0:
      return "All Time";
  }
};

export const countTypesMap = (countType: string) => {
  switch (countType) {
    case "sub":
      return "Subscriber";
    case "view":
      return "View";
  }
};