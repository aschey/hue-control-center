import { Button, List } from '@chakra-ui/react';
import React from 'react';
import { ListCard } from './ListCard';
import { SettingButton } from './SettingButton';

export const SettingList: React.FC<{}> = () => {
  return (
    <List spacing={3} p={5}>
      <SettingButton />
      <SettingButton />
    </List>
  );
};
