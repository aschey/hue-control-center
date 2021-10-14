import { ListItem } from '@chakra-ui/react';
import React from 'react';

export const ListCard: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ListItem
      borderRadius={5}
      boxShadow='0 4px 8px 0 rgba(0,0,0,0.2)'
      _hover={{ boxShadow: '0 8px 16px 0 rgba(0,0,0,0.2)' }}
    >
      {children}
    </ListItem>
  );
};
