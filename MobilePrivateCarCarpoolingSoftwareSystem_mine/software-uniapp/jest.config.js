module.exports = {
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['js', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.js$': 'babel-jest'
  },
  testEnvironmentOptions: {
    customExportConditions: ['node', 'node-addons']
  },
    transformIgnorePatterns: [
      '/node_modules/(?!(@dcloudio/uni-ui)/)' // <-- 允许对 uni-ui 进行转译
    ],
    moduleNameMapper: {
      // mock 所有 .vue 文件，包括 uni-ui
      '^@/(.*)$': '<rootDir>/$1',
      '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
      '^@dcloudio/uni-ui/lib/uni-popup/uni-popup.vue$': '<rootDir>/tests/__mocks__/uni-popup.js'
    },
  collectCoverage: true,
  collectCoverageFrom: [
    'pages/**/*.{js,vue}',
    '!**/node_modules/**',
    '!**/vendor/**'
  ]
};
