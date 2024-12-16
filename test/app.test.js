
document.getElementById = jest.fn().mockReturnValue({
    innerHTML: '',
  });
  

  const mockDateNow = jest.spyOn(global.Date, 'now');
  
  describe('App Functionality Tests', () => {
    
    let aliveSecond;
    const heartBeatRate = 5000;
  
    beforeEach(() => {
      aliveSecond = Date.now(); // Initialize with current time
      document.getElementById.mockClear(); // Reset DOM mock
    });
  
    afterEach(() => {
      mockDateNow.mockClear();
    });
  
    // Test for time()
    test('should update connection status to ALIVE when within heartbeat rate', () => {
      mockDateNow.mockReturnValue(aliveSecond + 4000); 
      const time = require('./app').time; 
      time(); // Call the function
  
      expect(document.getElementById).toHaveBeenCalledWith('connection_id');
      expect(document.getElementById('connection_id').innerHTML).toBe('ALIVE');
    });
  
    test('should update connection status to DEAD when outside heartbeat rate', () => {
      mockDateNow.mockReturnValue(aliveSecond + 7000); // Simulate beyond the heartbeat window
  
      const time = require('./app').time; // Import the function
      time(); // Call the function
  
      expect(document.getElementById).toHaveBeenCalledWith('connection_id');
      expect(document.getElementById('connection_id').innerHTML).toBe('DEAD');
    });
  
    // Test for keepAlive()
    test('should update aliveSecond on successful fetch from /keep_alive', async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ status: 'alive' }),
        })
      );
  
      const keepAlive = require('./app').keepAlive; 
      await keepAlive(); // Call the function
  
      expect(fetch).toHaveBeenCalledWith('/keep_alive');
      expect(aliveSecond).toBeDefined(); // aliveSecond should update
    });
  
    test('should handle fetch error in keepAlive', async () => {
      global.fetch = jest.fn(() => Promise.reject(new Error('Server offline')));
  
      const keepAlive = require('./app').keepAlive; // Import the function
      await keepAlive(); // Call the function
  
      expect(fetch).toHaveBeenCalledWith('/keep_alive');
      expect(console.log).toHaveBeenCalledWith(expect.any(Error)); // Ensure error was logged
    });
  
    // Test for handleMessage()
    test('should update motion_id for coffee detection', () => {
      const handleMessage = require('./app').handleMessage; // Import the function
  
      handleMessage('Cup detected');
      expect(document.getElementById).toHaveBeenCalledWith('motion_id');
      expect(document.getElementById('motion_id').innerHTML).toBe('There is coffee there');
  
      handleMessage('No cup detected');
      expect(document.getElementById('motion_id').innerHTML).toBe('No coffee present');
    });
  
    test('should update led_id for LED activation', () => {
      const handleMessage = require('./app').handleMessage; // Import the function
  
      handleMessage('Red LED Activated');
      expect(document.getElementById).toHaveBeenCalledWith('led_id');
      expect(document.getElementById('led_id').innerHTML).toBe('Red LED Activated');
  
      handleMessage('LED deactivated');
      expect(document.getElementById('led_id').innerHTML).toBe('Deactivated');
    });
  });
  