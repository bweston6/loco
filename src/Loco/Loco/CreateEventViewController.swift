//
//  CreateEventViewController.swift
//  Loco
//
//  Created by Rostom bnehamada on 4/16/22.
//  Copyright © 2022 Rostom bnehamada. All rights reserved.
//

import UIKit
import MapKit

class CreateEventViewController: UIViewController, MKMapViewDelegate{
    
    
    @IBOutlet weak var date: UIDatePicker!
    @IBOutlet weak var SearchAdress: UIButton!
    @IBOutlet weak var EventName: UITextField!
    @IBOutlet weak var StartTime: UITextField!
    
    @IBOutlet weak var radius: UITextField!
    @IBOutlet weak var Duration: UITextField!
    
    @IBOutlet weak var mapView: MKMapView!
    @IBOutlet weak var EventDescription: UITextView!
    
    @IBOutlet weak var Adress: UITextField!
    @IBAction func DeleteEvent(_ sender: Any) {
        mapView.removeAnnotations(mapView.annotations)
        
    }
    
    var eventInfo = (token : String() , lat : Double() , long : Double() , location : String() , title : String() , description : String() , radius : String() , duration : String() , hostemail : String() , emails : String() , startTime : Int()   )
    
    var name = "Ross"
    
    @IBAction func SearchAdress(_ sender: Any) {
        let request = MKLocalSearchRequest()
        request.naturalLanguageQuery = Adress.text
        request.region = mapView.region
        
        let search = MKLocalSearch(request: request)
        search.start(completionHandler: {(response, error) in
            if error != nil {
                print("Error occured in search")
            } else if response!.mapItems.count == 0 {
                print("No matches found")
            } else {
                print("Matches found")
                
                for item in response!.mapItems {
                    let annotation = MKPointAnnotation()
                    annotation.title = item.name
                    annotation.coordinate = item.placemark.coordinate
                    DispatchQueue.main.async {
                        self.mapView.addAnnotation(annotation)
                    }
                    
                    self.eventInfo.lat = annotation.coordinate.latitude
                    self.eventInfo.long = annotation.coordinate.longitude
                    self.eventInfo.location = annotation.title!
                    
            }
        }
        
    })
    }

    
    @IBAction func CreateEvent(_ sender: Any) {//sned all data of event back to event display
        eventInfo.title = EventName.text!
        eventInfo.description = EventDescription.text
        eventInfo.radius = radius.text!
        eventInfo.duration = Duration.text!
        let TimeStamp = self.date?.date.timeIntervalSince1970
        eventInfo.startTime = Int(TimeStamp!)
        
        performSegue(withIdentifier: "ReturnToHome", sender: Any?.self)
        
            }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if (segue.identifier == "ReturnTohome") {
            let destinationVC = segue.destination as! HostMainViewController
            destinationVC.eventInfo = eventInfo
        }
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        radius.placeholder = "Radius"
        EventName.placeholder = "Enter event Name"
        Duration.placeholder = "Duration"
        Adress.placeholder = "Adress"
        
       
        
      
        
    }

    

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

}


