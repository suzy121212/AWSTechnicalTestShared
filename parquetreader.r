#Parquet Reader

#Use credentials via the Instance Profile associated to the IAM Role
#Read the parquet file in the S3 bucket, and print out the second record in the parquet file to standard error.

main <- function() {
        args <- commandArgs(trailingOnly = TRUE)
        
        virtualenviron <- args[1]
        bucket<- args[2]
        key <- args[3]
        
        cat(virtualenviron)
        
        parquetreader(virtualenviron,bucket,key)
}

parquetreader <- function(virtualenviron,bucket,key){
        
        packages <- c("s3fs","pyarrow","pandas")
        
        #Create virtual environment
        reticulate::virtualenv_create(virtualenviron)
        
        #Install required packages
        reticulate::virtualenv_install(virtualenviron,packages)
        
        #Set virtual environment
        reticulate::use_virtualenv(virtualenviron,required=TRUE)
        
        s3fs<-reticulate::import("s3fs")
        pq<-reticulate::import("pyarrow.parquet")
        pandas<-reticulate::import("pandas")
        
        #Set path
        path<- paste("s3:/",bucket,key,sep="/")
        
        #Interface for S3 bucket
        s3 <- s3fs$S3FileSystem()
        
        #Read table from Parquet format and convert to dataframe
        df <- pq$ParquetDataset(path, filesystem=s3)
        df<-df$read_pandas()$to_pandas()
        
        #Return second row
        df<-df[2,]
        
        return(df)
        
}

main()
