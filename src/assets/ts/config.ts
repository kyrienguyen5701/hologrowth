import config from "@/assets/json/configuration.json";
import { Configuration } from "./interfaces";

export function GetConfig()
{
    return config as Configuration; 
}