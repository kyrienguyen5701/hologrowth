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
  channelId: string;
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

export interface SongData {
  name: LanguageData;
  path: string;
}