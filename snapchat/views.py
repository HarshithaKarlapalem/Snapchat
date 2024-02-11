from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import cv2
import os
import  matplotlib.pyplot as plt
import shutil

userID = {}
currentUSR = ""
count=0

def home(request):    
    return render(request,'home.html')

def signIn(request):
    global currentUSR
    user=""
    if request.method == "POST":
        user = request.POST.get("name", "")
    
    
    #user = input("Enter user ID: ")
    if user in userID:
        if request.method == "POST":
            psd = request.POST.get("password", "")
        #psd = input("Enter password: ")
        if psd == userID[user]:
            currentUSR = user
            return HttpResponseRedirect('user')          
        else:
           # print("Incorrect password.")
           render(request, 'signin.html', {'success_message': 'Sign in unsuccessful'})
    return render(request,'signin.html')


def signUp(request):
    if request.method == "POST":
        user = request.POST.get("name", "")
        psd = request.POST.get("password", "")
        p = request.POST.get("reenter", "")

        if psd != p:
            # Passwords do not match, handle this case (e.g., return an error message).
            return render(request, 'signup.html')

        parent_dir = os.getcwd()

        # Create the 'coding' directory if it doesn't exist
        os.makedirs(parent_dir, exist_ok=True)

        path = os.path.join(parent_dir, user)
        try:
            os.mkdir(path)
            # Directory created successfully.
        except FileExistsError:
            print("Directory '%s' already exists" % user)

        userID[user] = psd
        #signIn(request)
        return HttpResponseRedirect('LoginIn')  

    return render(request, 'signup.html')

def snap():
    
    output_directory = os.path.join(os.getcwd(), currentUSR)  # Use the current working directory

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)  # Create the directory if it doesn't exist

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)

    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("press space to take a photo", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            nam=""+count+"snap"+currentUSR
            count+=1
            img_name = os.path.join(output_directory, nam+".jpg".format(img_counter))
            if cv2.imwrite(img_name, frame):
                print("{} written!".format(img_name))
                img_counter += 1
            else:
                print("Failed to write image.")
    cam.release()
    cv2.destroyAllWindows()

def view():
    global currentUSR
    folder_path = os.getcwd()+currentUSR
    files = os.listdir(folder_path)

# Iterate over the files and print their names
    for file in files:
        print(file)
    image_name = input("Enter image name: ")+".jpg"  # Change to the name of your image file

    # Construct the full path to the image file
    image_path = os.path.join(folder_path, image_name)

    # Check if the image file exists
    if os.path.isfile(image_path):
        # Read the image using OpenCV
        image = cv2.imread(image_path)

        if image is not None:
            # Display the image
            cv2.imshow("Image Viewer", image)

            # Wait for a key press and close the window
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Failed to read the image.")
    else:
        print(f"Image '{image_name}' not found in the folder.")

def sendTo():
    global currentUSR
    folder_path = os.getcwd()+"/"+currentUSR
    files = os.listdir(folder_path)
    imgname=input("Enter image name: ")+".jpg"
    usr=input("Enter user ID: ")
    if usr in userID:
        folder_path = os.getcwd()+"/"+usr
        files = os.listdir(folder_path)
        img_name = os.path.join(folder_path, imgname)
        if os.path.isfile(img_name):
            print("Image already exists")
        else:
            # img_name = os.path.join(folder_path, imgname)
            # img_name1 = os.path.join(os.getcwd()+"/"+currentUSR, imgname)
            # os.rename(img_name1, img_name)
            # print("Image sent")
            # Define your source and destination paths
            img_name1 = os.path.join(os.getcwd() + "/" + currentUSR, imgname)
            img_name = os.path.join(folder_path, imgname)

            # Copy the image file from source to destination
            shutil.copy2(img_name1, img_name)

            print("Image copied and sent")
    else:
        print("User does not exist")
    


def user(request):
    if request.method == "POST":
        if 'takeIMG' in request.POST:
            return snap()
        elif 'viewIMG' in request.POST:
            return view()
        elif 'Send' in request.POST:
            return sendTo()
        elif 'Quit' in request.POST:
            return HttpResponseRedirect('home')
    return render(request,'user.html')

def homeredirect(request):
    if request.method == 'POST':
        if 'signIn' in request.POST:
            return signIn(request)
        elif 'signUp' in request.POST:
            return signUp(request)


