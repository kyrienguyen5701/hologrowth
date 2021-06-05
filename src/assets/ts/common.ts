import * as interfaces from "./interfaces";

export function GetCSSVar(name: string) {
  return getComputedStyle(document.documentElement).getPropertyValue(name);
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
