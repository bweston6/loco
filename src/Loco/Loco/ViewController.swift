//
//  ViewController.swift
//  Loco
//
//  Created by Rostom bnehamada on 4/8/22.
//  Copyright © 2022 Rostom bnehamada. All rights reserved.
//

import UIKit

class ViewController: UIViewController,UIPickerViewDelegate,UIPickerViewDataSource {
    
    @IBOutlet weak var LogoImg: UIImageView!

    @IBOutlet weak var Email_input: UITextField!
    
    @IBOutlet weak var FullName: UITextField!
    
    @IBOutlet weak var UserType: UIPickerView!
    
    
    
    @IBAction func checkOTP(_ sender: Any) {
        if (OTP.text?.count == 6 ) {
            LoginButton.isHidden = false
        } else {
            OTP.text = "Wrong OTP try again please"
        }
    }
    
    @IBOutlet weak var checkOTPbutton: UIButton!
    
    
    var token = [String]()
    
    @IBAction func Login(_ sender: Any) {

            var json: [String: Any] = ["email": Email_input.text,"OTP":OTP.text,"fullName":FullName.text,"hostFlag":true]
            let jsonData = try? JSONSerialization.data(withJSONObject: json)
            let url = URL(string: "https://loco.bweston.uk/api/createUser")!
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.httpBody = jsonData
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        
        
        let task = URLSession.shared.dataTask(with: request) {data, response, error in
            
                let decoder = JSONDecoder()
                do{
                    let answerjson = try decoder.decode(answer.self, from: data!)
                    self.token.append(answerjson.token)
                }
                
                catch {
                    print(error)
                }
            }
            task.resume()
        print (token)
        
        if selectedOption == "Host" {
            /*func prepare(for segue: UIStoryboardSegue, sender: Any?) {
                if segue.identifier == "Host" {
                    let destination = segue.destination as! CreateEventViewController
                    
                    destination.an = answerjson.token
}            } */
            performSegue(withIdentifier: "toHost", sender: Any?.self)
        }
        else if selectedOption == "User" {
            performSegue(withIdentifier: "toUser", sender: Any?.self)
        }

    }
    
    @IBOutlet weak var OTP: UITextField!
    @IBOutlet weak var LoginButton: UIButton!
    
    @IBAction func emailAuth(_ sender: Any) {
        if ((Email_input) != nil && (Email_input.text) != "" && (Email_input.text) != "Email :"){
            var json: [String: Any] = ["email": Email_input.text]
            
            let jsonData = try? JSONSerialization.data(withJSONObject: json)
            let url = URL(string: "https://loco.bweston.uk/api/authenticateEmail")!
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = jsonData
            
            NSURLConnection.sendAsynchronousRequest(request, queue: OperationQueue.main) {(response, data, error) in
                guard let data = data else { return }
                print(String(data: data, encoding: .utf8)!)
                
            }
            
        }
        OTP.isHidden = false
        checkOTPbutton.isHidden = false
        
        
        
    }
    
    
    var pickerOption = [String]()
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
        
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return pickerOption.count
    }
    
    
    var selectedOption: String = ""
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) ->String? {
        selectedOption = pickerOption[row]
        return pickerOption[row]
    }
    

    override func viewDidLoad(){
        
        super.viewDidLoad()
        LoginButton.isHidden = true
        LogoImg.image = UIImage(named: "Loco.png")
        UserType.dataSource = self
        UserType.delegate = self
        pickerOption = ["User","Host"]
        OTP.isHidden = true
        checkOTPbutton.isHidden = true
        
        
    
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
        
    }
    

    
}
