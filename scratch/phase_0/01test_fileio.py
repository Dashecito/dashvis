import csv
import sys
import time  # 1. Import the time module
            

with open("01csvfile.csv", "a", newline='') as file: 
    
    writer = csv.DictWriter(file, fieldnames=["name", "home"])

    print("--- CSV Writer Started ---")
    print("Press Ctrl+C at any time to save and exit.\n")

    try:
        while True:
            name = input("What's your name? ")
            home = input("What's your home? ")
            writer.writerow({"name": name, "home": home})
            print(f"Saved: {name} from {home}\n")
            
    except KeyboardInterrupt:
        # 2. Start the stopwatch the exact millisecond you press Ctrl+C
        print("\n\nCtrl+C detected! Starting shutdown sequence...")
        start_time = time.time() 
        
        # 3. Force the flush
        print("Flushing data to hard drive...")
        file.flush() 
        
        # 4. Stop the stopwatch and calculate the difference
        flush_time = time.time()
        print(f"Flush complete! It took {flush_time - start_time:.4f} seconds.")
        
        print("Evacuating the script...")
        sys.exit(0)