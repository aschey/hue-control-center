import { extendTheme } from '@chakra-ui/react';

export const theme = extendTheme({
  config: {
    initialColorMode: 'dark',
  },
  colors: {
    baseBackground: '#011627',
    whiteAlpha: {
      900: '#abc6d1',
    },
    gray: {
      100: '#97aeb8',
    },
  },
});
