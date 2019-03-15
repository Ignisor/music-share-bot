from core.urls import MusicUrl                                                                                                                                    


murl = MusicUrl('https://music.youtube.com/watch?v=6hUkyKBsGtQ')                                                                                                  
name = murl.get_name()                                                                                                                                            

print(name)
