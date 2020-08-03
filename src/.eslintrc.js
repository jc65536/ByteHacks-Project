module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: 'babel-eslint'
  },
  extends: [
    '@nuxtjs'
  ],
  plugins: [
  ],
  // add your custom rules here
  rules: {
    indent: 'off',
    import: {
      default: 'off'
    },
    curly: 'off',
    'comma-dangle': 'off',
    "vue/no-unused-vars": "off",
    "semi": "off",
    "no-trailing-spaces": 0,
    "vue/require-v-for-key": 0,
    "no-unused-vars": "off",
    "vue/no-unused-components": 0,
    "quotes": 0,
    "space-before-function-paren": 0,
    "no-var": 0,
    "padded-blocks": 0,
    "eol-last": 0,
    "vue/valid-v-for": 0,
    "no-multi-spaces": 0
  }
}
