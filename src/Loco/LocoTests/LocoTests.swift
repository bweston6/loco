//
//  LocoTests.swift
//  LocoTests
//
//

import XCTest
@testable import Loco

class LocoTests: XCTestCase {
    
    
    
    func testExample() {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
    }
    
    func testPerformanceExample() {
        // Performance tests for running speeds and elapsed times.
        self.measure {
            metrics: [
      XCTClockMetric(), 
      XCTCPUMetric(),
      XCTStorageMetric(), 
      XCTMemoryMetric()
    ]
        }
    }
    
}
