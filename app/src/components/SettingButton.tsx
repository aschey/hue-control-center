import { Button } from '@chakra-ui/react';
import React from 'react';
import { ListCard } from './ListCard';

export const SettingButton: React.FC<{}> = () => {
  return (
    <ListCard>
      <Button colorScheme='blue' width='200px'>
        Test
      </Button>
    </ListCard>
  );
};