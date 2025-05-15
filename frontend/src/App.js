import React, { lazy, Suspense } from 'react';
import { ChakraProvider, Box, Spinner, Center } from '@chakra-ui/react';
import './App.css';

// Lazy load the GlobeView component for better performance
const GlobeView = lazy(() => import('./Globeview'));

function App() {
  return (
    <ChakraProvider>
      <Suspense fallback={
        <Center h="100vh" w="100vw">
          <Spinner size="xl" thickness="4px" speed="0.65s" color="blue.500" />
        </Center>
      }>
        <Box className="App">
          <GlobeView />
        </Box>
      </Suspense>
    </ChakraProvider>
  );
}

export default App;
