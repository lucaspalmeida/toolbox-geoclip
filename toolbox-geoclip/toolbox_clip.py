import os
arcpy.CheckOutExtension("Spatial")
input_folder = arcpy.GetParameterAsText(0)
feature_mask = arcpy.GetParameter(1)
output_folder = arcpy.GetParameterAsText(2)

# COLETANDO ARQUIVOS NO INPUT_FOLDER

#def toolbox_clip(input_folder,feature_mask,output_folder):
arcpy.env.workspace = input_folder

dirlist = os.listdir(input_folder)
shplist = []
tiflist = []

for item in dirlist:
    if item[-4:] == '.shp':
        shplist.append(item)
    if item[-4:] == '.tif':
        tiflist.append(item)

# CORTANDO OS ARQUIVOS COM FEIÇÕES VETORIAIS E POLIGONAIS

if len(shplist) != 0:
    for item in shplist:
        arcpy.Clip_analysis(item,feature_mask,output_folder+
                            '\\'+'clip_'+str(item)+'.shp')

# INCLUINDO CAMPO COM ÁREA (KM²) DAS FEIÇÕES RECORTADAS E SALVANDO

dirlist1 = os.listdir(output_folder)
shplist1 = []
        
for item in dirlist1:
    extension = arcpy.Describe(output_folder+'\\'+item).extension
    if extension == 'shp':
        shplist1.append(item)
                
for item in shplist1:
    shapetype = arcpy.Describe(output_folder+'\\'+item).shapeType
    if shapetype == 'Polygon':
        arcpy.AddField_management(output_folder+'\\'+item,"AREA_NOVA",
                                  "DOUBLE")
        calc = "{0}".format("!SHAPE.area@SQUAREKILOMETERS!")        
        arcpy.CalculateField_management(output_folder+'\\'+item,"AREA_NOVA",
                                        calc,"PYTHON",)

mxd = arcpy.mapping.MapDocument('current')
df = arcpy.mapping.ListDataFrames(mxd)[0]
for item in shplist1:
    arcpy.mapping.AddLayer(df,arcpy.mapping.Layer(output_folder+'\\'+item))

# CORTANDO OS ARQUIVOS COM FEIÇÕES MATRICIAIS E SALVANDO

if len(tiflist) != 0:
    for item in tiflist:
        outExtractByMask = arcpy.sa.ExtractByMask(item,feature_mask)
        outExtractByMask.save(output_folder+'\\'+'maskextract_'+
                              str(item))

# CONSTRUINDO PIRÂMIDES DOS ARQUIVOS COM FEIÇÕES MATRICIAIS

dirlist2 = os.listdir(output_folder)
tiflist1 = []
        
for item in dirlist2:
    extension = arcpy.Describe(output_folder+'\\'+item).extension
    if extension == 'tif':
        tiflist1.append(item)

    for item in tiflist1:
        arcpy.management.BuildPyramids(output_folder+'\\'+item)

for item in tiflist1:
    arcpy.mapping.AddLayer(df,arcpy.mapping.Layer(output_folder+'\\'+item),"TOP")
