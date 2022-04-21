//
//  HostMainViewController.swift
//  Loco
//
//  Created by Rostom bnehamada on 4/15/22.
//  Copyright © 2022 Rostom bnehamada. All rights reserved.
//

import UIKit

class HostMainViewController: UIViewController,UITableViewDelegate,UITableViewDataSource {
    @IBOutlet weak var EventTable: UITableView!
    
     var eventInfo = (token : String() , lat : Double() , long : Double() , location : String() , title : String() , description : String() , radius : String() , duration : String() , hostemail : String() , emails : String() , startTime : Int()   )
    

    var name = String()
    
    @IBAction func AddEvent(_ sender: Any) {
        performSegue(withIdentifier: "toCreateEvent", sender: Any?.self)
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        var mycell = tableView.dequeueReusableCell(withIdentifier:"cellEvent", for: indexPath)
        mycell.textLabel?.text = eventInfo.title
        return mycell
    }
    


    
    override func viewDidLoad() {
        
     
        print(eventInfo.title)
        print(eventInfo.description)
        print(eventInfo.lat)
        super.viewDidLoad()
  
        print(name)
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
