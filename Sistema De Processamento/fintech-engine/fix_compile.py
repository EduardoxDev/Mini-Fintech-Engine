import os
import glob

base_dir = "c:/Users/Purple/Downloads/Sistema De Processamento/fintech-engine/src/main/java/com/example/demo"

# Fix IdempotencyKeyEntity to be public
idemp_file = f"{base_dir}/infrastructure/persistence/IdempotencyKeyRepository.java"
with open(idemp_file, "r") as f:
    content = f.read()
content = content.replace("class IdempotencyKeyEntity {", "public class IdempotencyKeyEntity {")
with open(idemp_file, "w") as f:
    f.write(content)

# Add explicit logs where @Slf4j was used
def add_logger(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    if "@Slf4j" in content:
        content = content.replace("@Slf4j", "")
        content = content.replace("import lombok.extern.slf4j.Slf4j;", "import org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;")
        
        # Insert logger inside the class
        class_dec = content.find("public class")
        open_brace = content.find("{", class_dec) + 1
        class_name = content[class_dec:open_brace].split("class")[1].split("{")[0].strip().split(" ")[0]
        logger_stmt = f"\n    private static final Logger log = LoggerFactory.getLogger({class_name}.class);\n"
        content = content[:open_brace] + logger_stmt + content[open_brace:]
        
        with open(filepath, "w") as f:
            f.write(content)

add_logger(f"{base_dir}/core/usecase/TransferUseCase.java")
add_logger(f"{base_dir}/infrastructure/integration/AntiFraudService.java")

# For domain classes using Lombok, let's just downgrade Lombok plugin or upgrade it.
# Actually, the maven-compiler-plugin needs lombok annotationProcessorPaths in pom.xml.
# Our `generate_advanced.py` didn't add maven-compiler-plugin with lombok annotationprocessor. Spring Boot 3 + Lombok requires explicitly adding the annotation processor if we customize maven-compiler-plugin, or we just rely on standard spring-boot-starter-parent.
# Let's fix pom.xml to addlombok annotation processor.

pom_file = "c:/Users/Purple/Downloads/Sistema De Processamento/fintech-engine/pom.xml"
with open(pom_file, "r") as f:
    pom = f.read()

lombok_plugin = """
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<configuration>
					<annotationProcessorPaths>
						<path>
							<groupId>org.projectlombok</groupId>
							<artifactId>lombok</artifactId>
							<version>1.18.30</version>
						</path>
					</annotationProcessorPaths>
				</configuration>
			</plugin>
"""
if "maven-compiler-plugin" not in pom:
    pom = pom.replace("<plugins>", f"<plugins>\n{lombok_plugin}")
    with open(pom_file, "w") as f:
        f.write(pom)

# Print success
print("Fixed Lombok and permissions.")
