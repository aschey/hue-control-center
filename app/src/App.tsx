import React from 'react';
import logo from './logo.svg';
import tauriCircles from './tauri.svg';
import tauriWord from './wordmark.svg';
import {
  List,
  Box,
  ListIcon,
  Button,
  Flex,
  Grid,
  Container,
  FormControl,
  FormLabel,
  NumberInput,
  NumberInputField,
  NumberIncrementStepper,
  NumberInputStepper,
  NumberDecrementStepper,
  Select,
} from '@chakra-ui/react';
import './App.css';
import { SettingList } from './components/SettingList';

const App: React.FC<{}> = () => {
  return (
    <Grid bg='gray.600' w='100%' h='100%' autoRows='auto'>
      <Flex align='center' flexDirection='column'>
        <SettingList />
      </Flex>
      <Box p={5}>
        <Container
          minHeight='100%'
          borderRadius='5px'
          borderColor='gray.100'
          borderWidth='1px'
        >
          <FormControl>
            <FormLabel>Change Interval</FormLabel>
            <Flex>
              <NumberInput>
                <NumberInputField />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
              <Select placeholder='Select option'>
                <option value='seconds'>Seconds</option>
                <option value='minutes'>Minutes</option>
                <option value='hours'>Hours</option>
              </Select>
            </Flex>
            <FormLabel>Delay Interval</FormLabel>
            <Flex>
              <NumberInput>
                <NumberInputField />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
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
