# Hologrowth

Hololive Fanwork: Unofficial Data Tracker + Music Player

[Homepage](https://hologrowth.kyrie5701.com)

## Contributing

Please fork this project and initiate a Pull Request with a short description of what changes you have made.

## Requirements

* `node >= 14`
* `Vue >= 2`

## Project Setup

### Installs required packages

```cmd
yarn install
```

### Compiles and hot-reloads for development

```cmd
yarn serve
```

### Prettify

```cmd
yarn lint
```

## Site translation

Please put your translation using the below format in [here](/src/assets/json/localize.json) and use `GetLocalizedText` from `src/assets/ts/localize.ts` to translate.

```json
"name": {
    "jp": "日本語",
    "en": "English"
}
```

## Assets

### Images

Upload to folders of respective talents, using old pictures' names.

### Music

Upload songs to folders of respective talents and update metadata in both `src/assets/json/talents.json` for actually adding songs to the player and `src/assets/json/songs.json` for translation. Please refrain from uploading cover songs as we are unlikely to have the permission from the original artists.

## TODO

* Add a section for fun facts (if I have the time and dedication)
* Add annotations for charts (again, same thing)
* Improve UX (not loading when data disabled is one thing)
* ...

## License

This project is a work of enthusiasts and is not affiliated with Hololive Production or Cover Co., Ltd. This project is licensed under MIT license.

## Afterwords

A really fun and somewhat challenging project to work at since I have no experience with everything used for this one (except Python). Kudos to ntnam11 for his hard-work with Sass and UI.

## Update

### April 30th, 2023

Static files are move to Google Cloud Storage to speed up building.
