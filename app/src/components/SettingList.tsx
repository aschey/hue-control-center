import { List } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { getJson } from '../util/fetchUtil';
import { SettingButton } from './SettingButton';

export const SettingList: React.FC<{}> = () => {
  const [scripts, setScripts] = useState<string[]>([]);
  useEffect(() => {
    getJson<string[]>('http://localhost:5000/scripts/').then(setScripts);
  }, []);

  return (
    <List spacing={3} p={5}>
      {scripts.map((s) => (
        <SettingButton name={s} />
      ))}
    </List>
  );
};
