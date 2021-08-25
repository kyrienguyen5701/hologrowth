import { tickAmount } from './common';
// interface Object {
//   ContainsKey(searchKey: string): boolean;
// }

// Object.prototype.ContainsKey = function(searchKey: string) {
//   return Object.keys(this).includes(searchKey);
// };

export interface Configuration {
  languages: string[];
}

export interface TalentData {
  branch: string;
  genNumber: string;
  genName: string;
  genOther: string[];
  name: string;
  basicInfo: TalentBasicInfo;
  officialBio: string;
  tags: Array<string>;
  channelId: string;
  twitter: string;
  officialWebsiteEN: string;
  officialWebsiteJP: string;
}

export enum DataType {
  Branch,
  GenNumber,
  GenName,
  GenOther,
  Name,
  ChannelId
}

export interface Dictionary<T> {
  [Key: string]: T;
}

export interface BranchMenuData {
  branchName: string;
  branchGenData: GenMenuData[];
}

export interface GenMenuData {
  genName: string;
  genMember: MemberMenuData[];
}

export interface MemberMenuData {
  memberDisplayName: string;
  memberName: string;
  memberURL: string;
}

export interface LanguageData {
  jp?: string;
  en?: string;
}

export enum LocalizationType {
  Text,
  Song
}

export enum MonthAbbrv {
  Jan,
  Feb,
  Mar,
  Apr,
  May,
  Jun,
  Jul,
  Aug,
  Sep,
  Oct,
  Nov,
  Dec
}

export interface SongData {
  name: LanguageData;
  path: string;
}

export interface CurrentSong {
  name: string;
  audio: HTMLAudioElement;
}

export interface TalentDisplay {
  rel: number;
  name: string;
  avatar: object;
  banner: object;
  dataAvailable: boolean;
  shown: boolean;
}

export interface TalentBasicInfo {
  debutDate: string;
  age: string;
  birthday: string;
  height: string;
  zodiacSign: string;
}

export interface XAxis {
  categories: Array<string>;
  labels: {
    formatter: Function
  };
  tickAmount: number;
}