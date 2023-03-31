module.exports = function(api) {
    api.cache(false);
    const presets = [
        ["@babel/preset-env", {
            "targets": {
                "ie": "8"
            },
            "useBuiltIns": "entry"
        }]
    ];
    const plugins = [];

    return {presets, plugins};
}