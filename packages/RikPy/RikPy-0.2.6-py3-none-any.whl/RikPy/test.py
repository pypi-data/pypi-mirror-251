from commonheroku import heroku_upload_file_from_url

# Test the function with your URLs
dallefile = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-4crfjbsW4FCdUgyk3a8GcUvR/user-ECHPMxvKeRuTQtLTHCu5qaAU/img-RRsviiNw6uHPUbA9sdabkJOy.png?st=2024-01-17T11%3A00%3A43Z&se=2024-01-17T13%3A00%3A43Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-16T22%3A43%3A45Z&ske=2024-01-17T22%3A43%3A45Z&sks=b&skv=2021-08-06&sig=qHOicaZMXphFlcsjPsyESiCGqkmmb9n5T44VzxlkeXw%3D"
leonardofile = "https://cdn.leonardo.ai/users/d71165a1-5a13-415e-af90-543e909ea431/generations/bb54ed78-07cd-4de1-8578-512584c07e0b/Leonardo_Diffusion_XL_Create_an_abstract_image_featuring_lusci_0.jpg"


heroku_upload_file_from_url(file_url=dallefile, folder="borrar", bnewname=True)

# product_post_image="https://files.canvas.switchboard.ai/4ea249ec-1808-4a19-afd7-0a251a8d8aaf/dea12574-80f5-4b72-a853-8c9a8d40fc9f.png"
# profile_topic="wine"
# response=heroku_upload_file_from_url(product_post_image, profile_topic, heroku_config_dict)
# print(response)
