import React from 'react';
import {
  Box,
  Flex,
  Grid,
  Container,
  FormControl,
  FormLabel,
  Select,
} from '@chakra-ui/react';
import './App.css';
import { SettingList } from './components/SettingList';
import { TimeInput } from './components/TimeInput';

const App: React.FC<{}> = () => {
  return (
    <Grid bg='baseBackground' w='100%' h='100%' autoRows='auto'>
      <Flex align='center' flexDirection='column'>
        <SettingList />
      </Flex>
      <Box p={5}>
        <Container
          minHeight='100%'
          borderRadius='lg'
          borderColor='gray.100'
          borderWidth='1px'
        >
          <FormControl>
            <FormLabel>Change Interval</FormLabel>
            <Flex>
              <TimeInput />
              <Select placeholder='Select option'>
                <option value='seconds'>Seconds</option>
                <option value='minutes'>Minutes</option>
                <option value='hours'>Hours</option>
              </Select>
            </Flex>
            <FormLabel>Delay Interval</FormLabel>
            <Flex>
              <TimeInput />
              <Select placeholder='Select option'>
                <option value='seconds'>Seconds</option>
                <option value='minutes'>Minutes</option>
                <option value='hours'>Hours</option>
              </Select>
            </Flex>
          </FormControl>
        </Container>
      </Box>
    </Grid>
  );
};

export default App;
