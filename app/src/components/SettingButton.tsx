import { Button } from '@chakra-ui/react';
import React from 'react';
import { ListCard } from './ListCard';

export const SettingButton: React.FC<{ name: string }> = ({ name }) => {
  return (
    <ListCard>
      <Button width='200px'>{name}</Button>
    </ListCard>
  );
};
